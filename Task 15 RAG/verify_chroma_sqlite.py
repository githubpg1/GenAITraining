"""Inspect Chroma persistence without loading its crashing native index runtime."""
import sqlite3
from src.config import PROJECT_ROOT, settings


def verify() -> int:
    path = PROJECT_ROOT / "chroma_db" / "chroma.sqlite3"
    if not path.exists():
        print("status=FAIL")
        print("reason=chroma.sqlite3 is missing")
        return 1
    connection = sqlite3.connect(path)
    collection = connection.execute(
        "select name, dimension from collections where name = ?",
        (settings.chroma_collection_name,),
    ).fetchone()
    if not collection:
        print("status=FAIL")
        print(f"reason=collection {settings.chroma_collection_name} is missing")
        connection.close()
        return 1
    count = connection.execute(
        "select count(*) from embeddings where segment_id in "
        "(select id from segments where collection = "
        "(select id from collections where name = ?))",
        (settings.chroma_collection_name,),
    ).fetchone()[0]
    sources = connection.execute(
        "select distinct em.string_value from embedding_metadata em "
        "join embeddings e on e.id = em.id "
        "join segments s on s.id = e.segment_id "
        "where em.key = 'source_file' and s.collection = "
        "(select id from collections where name = ?) order by em.string_value",
        (settings.chroma_collection_name,),
    ).fetchall()
    versions = connection.execute(
        "select distinct em.string_value from embedding_metadata em "
        "join embeddings e on e.id = em.id "
        "join segments s on s.id = e.segment_id "
        "where em.key = 'version' and s.collection = "
        "(select id from collections where name = ?) order by em.string_value",
        (settings.chroma_collection_name,),
    ).fetchall()
    print(f"collection={collection[0]}")
    print(f"dimension={collection[1]}")
    print(f"embedding_count={count}")
    print("source_files=")
    for (source,) in sources:
        print(f"- {source}")
    print("versions=")
    for (version,) in versions:
        print(f"- {version}")
    expected = {
        "employee_time_off_policy_2026.pdf",
        "employee_time_off_policy_2025.pdf",
        "business_travel_expense_policy_2026.pdf",
        "parental_leave_policy_2026.pdf",
        "employee_benefits_policy_2026.pdf",
    }
    actual = {source for (source,) in sources}
    missing = sorted(expected - actual)
    print(f"missing_expected_sources={missing}")
    print("status=PASS" if not missing else "status=FAIL")
    connection.close()
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(verify())
