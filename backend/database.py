import json
import psycopg2
import psycopg2.extras
from pgvector.psycopg2 import register_vector
from config import DATABASE_URL
from models.schemas import FailureRecord


def _raw_connection():
    """Get a connection WITHOUT registering vector (for bootstrapping)."""
    return psycopg2.connect(DATABASE_URL)


def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)
    return conn


def init_db():
    # First, create the extension with a raw connection (before register_vector)
    conn = _raw_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    conn.close()

    # Now that the extension exists, use the full connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS failures (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            domain TEXT NOT NULL,
            subdomain TEXT,
            year INTEGER,
            organization TEXT,
            what_failed TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            root_cause_category TEXT NOT NULL,
            warning_signs TEXT NOT NULL,
            what_was_done_wrong TEXT NOT NULL,
            how_it_was_fixed TEXT,
            lesson TEXT NOT NULL,
            severity TEXT NOT NULL,
            source_url TEXT,
            tags TEXT NOT NULL,
            related_failure_ids TEXT NOT NULL DEFAULT '[]',
            embedding vector(384)
        )
    """)
    conn.commit()
    conn.close()


def _row_to_record(row: dict) -> FailureRecord:
    return FailureRecord(
        id=row["id"],
        title=row["title"],
        domain=row["domain"],
        subdomain=row["subdomain"],
        year=row["year"],
        organization=row["organization"],
        what_failed=row["what_failed"],
        root_cause=row["root_cause"],
        root_cause_category=row["root_cause_category"],
        warning_signs=json.loads(row["warning_signs"]),
        what_was_done_wrong=row["what_was_done_wrong"],
        how_it_was_fixed=row["how_it_was_fixed"],
        lesson=row["lesson"],
        severity=row["severity"],
        source_url=row["source_url"],
        tags=json.loads(row["tags"]),
        related_failure_ids=json.loads(row["related_failure_ids"]),
    )


def insert_failure(record: FailureRecord, embedding: list[float] = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO failures 
        (id, title, domain, subdomain, year, organization, what_failed, root_cause,
         root_cause_category, warning_signs, what_was_done_wrong, how_it_was_fixed,
         lesson, severity, source_url, tags, related_failure_ids, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            domain = EXCLUDED.domain,
            subdomain = EXCLUDED.subdomain,
            year = EXCLUDED.year,
            organization = EXCLUDED.organization,
            what_failed = EXCLUDED.what_failed,
            root_cause = EXCLUDED.root_cause,
            root_cause_category = EXCLUDED.root_cause_category,
            warning_signs = EXCLUDED.warning_signs,
            what_was_done_wrong = EXCLUDED.what_was_done_wrong,
            how_it_was_fixed = EXCLUDED.how_it_was_fixed,
            lesson = EXCLUDED.lesson,
            severity = EXCLUDED.severity,
            source_url = EXCLUDED.source_url,
            tags = EXCLUDED.tags,
            related_failure_ids = EXCLUDED.related_failure_ids,
            embedding = EXCLUDED.embedding
        """,
        (
            record.id,
            record.title,
            record.domain,
            record.subdomain,
            record.year,
            record.organization,
            record.what_failed,
            record.root_cause,
            record.root_cause_category,
            json.dumps(record.warning_signs),
            record.what_was_done_wrong,
            record.how_it_was_fixed,
            record.lesson,
            record.severity,
            record.source_url,
            json.dumps(record.tags),
            json.dumps(record.related_failure_ids),
            embedding,
        ),
    )
    conn.commit()
    conn.close()


def get_failure_by_id(failure_id: str) -> FailureRecord | None:
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM failures WHERE id = %s", (failure_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return _row_to_record(row)


def get_all_failures(
    domain: str = None,
    severity: str = None,
    limit: int = 50,
    offset: int = 0,
) -> list[FailureRecord]:
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = "SELECT * FROM failures WHERE 1=1"
    params = []
    if domain:
        query += " AND domain = %s"
        params.append(domain)
    if severity:
        query += " AND severity = %s"
        params.append(severity)
    query += " ORDER BY year DESC NULLS LAST LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_record(row) for row in rows]


def get_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT COUNT(*) as total FROM failures")
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT domain, COUNT(*) as count FROM failures GROUP BY domain ORDER BY count DESC"
    )
    by_domain = {row["domain"]: row["count"] for row in cursor.fetchall()}

    cursor.execute(
        "SELECT root_cause_category, COUNT(*) as count FROM failures GROUP BY root_cause_category ORDER BY count DESC"
    )
    by_root_cause = {
        row["root_cause_category"]: row["count"] for row in cursor.fetchall()
    }

    cursor.execute(
        "SELECT severity, COUNT(*) as count FROM failures GROUP BY severity ORDER BY count DESC"
    )
    by_severity = {row["severity"]: row["count"] for row in cursor.fetchall()}

    conn.close()
    return {
        "total": total,
        "by_domain": by_domain,
        "by_root_cause": by_root_cause,
        "by_severity": by_severity,
    }


def failure_exists(failure_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM failures WHERE id = %s", (failure_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def update_related_failures(failure_id: str, related_ids: list[str]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE failures SET related_failure_ids = %s WHERE id = %s",
        (json.dumps(related_ids), failure_id),
    )
    conn.commit()
    conn.close()


def search_by_embedding(
    query_embedding: list[float],
    n_results: int = 10,
    filter_domain: str = None,
    filter_root_cause: str = None,
) -> list[dict]:
    """Perform vector similarity search using pgvector's cosine distance operator."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """
        SELECT id, title, domain, root_cause_category, severity,
               embedding <=> %s::vector AS distance
        FROM failures
        WHERE embedding IS NOT NULL
    """
    params = [str(query_embedding)]

    if filter_domain:
        query += " AND domain = %s"
        params.append(filter_domain)
    if filter_root_cause:
        query += " AND root_cause_category = %s"
        params.append(filter_root_cause)

    query += " ORDER BY distance ASC LIMIT %s"
    params.append(n_results)

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
    except Exception:
        conn.close()
        return []

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "distance": float(row["distance"]),
            "metadata": {
                "domain": row["domain"],
                "root_cause_category": row["root_cause_category"],
                "severity": row["severity"],
            },
        })
    conn.close()
    return results


def count_failures() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM failures")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def source_url_exists(source_url: str) -> bool:
    """Check if a failure with this source_url already exists."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM failures WHERE source_url = %s", (source_url,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
