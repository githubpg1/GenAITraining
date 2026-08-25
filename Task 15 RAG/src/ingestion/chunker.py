"""Section-aware, deterministic chunking."""
from dataclasses import dataclass
import hashlib
import re


@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict


def chunk_sections(sections, document_id: str, document_name: str, version: str,
                   effective_date: str, source_file: str, chunk_size: int = 650,
                   overlap: int = 100, page_number: int = 1) -> list[Chunk]:
    chunks: list[Chunk] = []
    for section_number, section_title, body in sections:
        words = re.findall(r"\S+", body)
        if not words:
            continue
        start = 0
        index = 1
        while start < len(words):
            end = min(start + chunk_size, len(words))
            text = f"{section_number} {section_title}\n{' '.join(words[start:end])}".strip()
            raw_id = f"{document_id}::{section_number or 'document'}::chunk-{index:03d}"
            chunk_id = hashlib.sha256(raw_id.encode()).hexdigest()[:24]
            chunks.append(Chunk(chunk_id, text, {
                "document_id": document_id,
                "document_name": document_name,
                "document_type": "HR_POLICY",
                "section": f"{section_number} {section_title}".strip(),
                "section_number": section_number or "N/A",
                "version": version,
                "effective_date": effective_date,
                "source_file": source_file,
                "page_number": page_number,
            }))
            if end == len(words):
                break
            start = max(end - overlap, start + 1)
            index += 1
    return chunks
