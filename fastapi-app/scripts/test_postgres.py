import sys
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.config import settings  # noqa: E402


def main() -> None:
    query = """
        SELECT id, name, description, date_insert, date_update
        FROM events.event;
    """

    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
