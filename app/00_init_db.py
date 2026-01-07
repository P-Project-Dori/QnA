"""
00_init_db.py
Initialize the database schema and sample data from SQL files.
Run this before any other seed scripts.
"""
import os
from pathlib import Path

import psycopg2

from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


def execute_sql_file(conn, sql_file_path):
    """Execute SQL statements from a file."""
    print(f"📄 Executing {sql_file_path}...")
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    with conn.cursor() as cur:
        # Execute the entire SQL file
        cur.execute(sql_content)
    conn.commit()
    print(f"✅ Completed {sql_file_path}")


def main():
    # Get the project root directory (parent of app/)
    project_root = Path(__file__).parent.parent
    db_dir = project_root / "db"
    
    schema_file = db_dir / "schema.sql"
    sample_data_file = db_dir / "sample_data.sql"
    
    # Check if files exist
    if not schema_file.exists():
        print(f"❌ Error: {schema_file} not found!")
        return
    
    if not sample_data_file.exists():
        print(f"❌ Error: {sample_data_file} not found!")
        return
    
    print("🔧 Initializing database...")
    print(f"   Database: {DB_NAME}")
    print(f"   Host: {DB_HOST}")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        
        # Execute schema first
        execute_sql_file(conn, schema_file)
        
        # Then execute sample data
        execute_sql_file(conn, sample_data_file)
        
        conn.close()
        print("\n✅ Database initialization complete!")
        print("   You can now run the seed scripts:")
        print("   - python app/01_seed_spots.py")
        print("   - python app/02_seed_knowledge_docs.py")
        print("   - python app/03_build_faiss_index.py")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()




