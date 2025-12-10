import json
from contextlib import contextmanager

import psycopg2

from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


@contextmanager
def get_conn():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    try:
        yield conn
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# spots / scripts helpers
# ---------------------------------------------------------------------------

def insert_spot(
    code: str,
    name_en: str,
    order_no: int,
    lat: float = None,
    lng: float = None,
    is_photo_spot: bool = False,
    place_id: str = "gyeongbokgung",
):
    """
    spot 코드 기준으로 INSERT 또는 UPDATE.
    """
    sql = """
        INSERT INTO spots (place_id, code, name_en, order_no, lat, lng, is_photo_spot)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (code) DO UPDATE
        SET place_id      = EXCLUDED.place_id,
            name_en       = EXCLUDED.name_en,
            order_no      = EXCLUDED.order_no,
            lat           = EXCLUDED.lat,
            lng           = EXCLUDED.lng,
            is_photo_spot = EXCLUDED.is_photo_spot;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (place_id, code, name_en, order_no, lat, lng, is_photo_spot),
            )
        conn.commit()


def insert_script_for_spot_code(spot_code, order_in_spot, text_en):
    """
    spot_code(예: 'gwanghwamun')로 spots.id를 찾아서 scripts에 INSERT.
    """
    sql_spot = "SELECT id FROM spots WHERE code = %s"
    sql_insert = """
        INSERT INTO scripts (spot_id, order_in_spot, text_en)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_spot, (spot_code,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Spot with code '{spot_code}' not found")
            spot_id = row[0]

            cur.execute(sql_insert, (spot_id, order_in_spot, text_en))
        conn.commit()


def get_scripts_for_spot_code(spot_code: str):
    """
    주어진 spot_code에 대한 scripts.text_en 목록을 순서대로 반환.
    """
    sql = """
        SELECT s.id, s.order_in_spot, s.text_en
        FROM scripts AS s
        JOIN spots AS sp ON s.spot_id = sp.id
        WHERE sp.code = %s
        ORDER BY s.order_in_spot ASC;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (spot_code,))
            rows = cur.fetchall()

    # 반환: [(order_in_spot, text_en), ...]
    return [(order_in_spot, text_en) for _id, order_in_spot, text_en in rows]


# ---------------------------------------------------------------------------
# knowledge_docs helpers
# ---------------------------------------------------------------------------

def insert_knowledge_doc_for_spot_code(
    spot_code: str,
    place_id: str,
    text: str,
    language: str,
    source_type: str,
    source_ref: str = None,
    tags=None,
):
    """
    주어진 spot_code, place_id에 대한 knowledge_docs 한 줄 INSERT.
    """
    if tags is None:
        tags = []

    sql_spot = "SELECT id FROM spots WHERE code = %s"
    sql_insert = """
        INSERT INTO knowledge_docs (
            spot_id, place_id, language, source_type, source_ref, text, tags
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_spot, (spot_code,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Spot with code '{spot_code}' not found")
            spot_id = row[0]

            cur.execute(
                sql_insert,
                (
                    spot_id,
                    place_id,
                    language,
                    source_type,
                    source_ref,
                    text,
                    json.dumps(tags),
                ),
            )
            new_id = cur.fetchone()[0]
        conn.commit()
    return new_id


def get_all_knowledge_docs(language: str = "en"):
    """
    지정한 language에 해당하는 모든 knowledge_docs를 반환.
    """
    sql = """
        SELECT id, text, spot_id, place_id, language, source_type, source_ref, tags
        FROM knowledge_docs
        WHERE language = %s
        ORDER BY id ASC;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (language,))
            rows = cur.fetchall()

    docs = []
    for row in rows:
        doc_id, text, spot_id, place_id, lang, source_type, source_ref, tags = row
        docs.append(
            {
                "id": doc_id,
                "text": text,
                "spot_id": spot_id,
                "place_id": place_id,
                "language": lang,
                "source_type": source_type,
                "source_ref": source_ref,
                "tags": tags,
            }
        )
    return docs


def get_knowledge_docs_by_ids(ids):
    """
    주어진 id 리스트에 해당하는 knowledge_docs를 반환.
    """
    if not ids:
        return []

    placeholders = ", ".join(["%s"] * len(ids))
    sql = f"""
        SELECT id, text, spot_id, place_id, language, source_type, source_ref, tags
        FROM knowledge_docs
        WHERE id IN ({placeholders})
        ORDER BY id;
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, ids)
            rows = cur.fetchall()

    docs = []
    for row in rows:
        doc_id, text, spot_id, place_id, lang, source_type, source_ref, tags = row
        docs.append(
            {
                "id": doc_id,
                "text": text,
                "spot_id": spot_id,
                "place_id": place_id,
                "language": lang,
                "source_type": source_type,
                "source_ref": source_ref,
                "tags": tags,
            }
        )
    return docs
