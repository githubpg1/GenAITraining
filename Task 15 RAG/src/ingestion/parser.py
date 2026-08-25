"""PDF extraction with page and section provenance."""
from dataclasses import dataclass
from pathlib import Path
import re
import fitz


@dataclass
class PageText:
    page_number: int
    text: str


@dataclass
class ParsedDocument:
    source_file: str
    pages: list[PageText]

    @property
    def text(self) -> str:
        return "\n".join(page.text for page in self.pages)


def parse_pdf(path: str | Path) -> ParsedDocument:
    path = Path(path)
    try:
        with fitz.open(path) as pdf:
            pages = [PageText(i + 1, page.get_text("text").strip()) for i, page in enumerate(pdf)]
    except Exception as exc:
        raise ValueError(f"Could not parse PDF '{path.name}': {exc}") from exc
    if not pages or not any(page.text for page in pages):
        raise ValueError(f"PDF '{path.name}' contains no extractable text; OCR may be required.")
    return ParsedDocument(path.name, pages)


SECTION_RE = re.compile(r"^\s*((?:\d+\.)+\d*|\d+)\s+(.+?)\s*$")


def detect_sections(text: str) -> list[tuple[str, str, str]]:
    sections: list[tuple[str, str, str]] = []
    current_number, current_title, buffer = "", "Document", []
    for line in text.splitlines():
        match = SECTION_RE.match(line)
        if match and len(match.group(2)) < 120:
            if buffer:
                sections.append((current_number, current_title, "\n".join(buffer).strip()))
            current_number, current_title, buffer = match.group(1), match.group(2), []
        else:
            buffer.append(line)
    if buffer:
        sections.append((current_number, current_title, "\n".join(buffer).strip()))
    return [(number, title, body) for number, title, body in sections if body]
