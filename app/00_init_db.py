"""
00_init_db.py
Initialize the database schema and sample data from SQL files.
Run this before any other seed scripts.
"""
import os
from pathlib import Path

import psycopg2

from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


def detect_file_encoding(file_path):
    """
    Detect the encoding of a file.
    Returns the detected encoding or None if detection fails.
    Useful for debugging encoding issues.
    Requires 'chardet' package (optional).
    """
    try:
        import chardet
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result.get('encoding'), result.get('confidence')
    except ImportError:
        return None, None  # chardet not installed
    except Exception:
        return None, None  # Detection failed


def execute_sql_file(conn, sql_file_path):
    """Execute SQL statements from a file.
    
    Handles UTF-8 encoding issues across different platforms.
    Supports both Path objects and string paths.
    """
    # Convert Path object to string if needed, and resolve to absolute path
    if isinstance(sql_file_path, Path):
        sql_file_path = sql_file_path.resolve()
    else:
        sql_file_path = Path(sql_file_path).resolve()
    
    print(f"📄 Executing {sql_file_path}...")
    
    # Try UTF-8 first (strict), then UTF-8-sig (for BOM), then with error handling
    # Use Path.open() for better cross-platform compatibility
    sql_content = None
    encoding_used = None
    
    # First, try strict UTF-8 (preferred)
    try:
        with sql_file_path.open("r", encoding="utf-8") as f:
            sql_content = f.read()
        encoding_used = "utf-8"
    except UnicodeDecodeError:
        # Try UTF-8 with BOM (some editors add BOM)
        try:
            with sql_file_path.open("r", encoding="utf-8-sig") as f:
                sql_content = f.read()
            encoding_used = "utf-8-sig"
        except UnicodeDecodeError:
            # Last resort: try with error replacement (shouldn't happen for properly saved files)
            try:
                with sql_file_path.open("r", encoding="utf-8", errors="replace") as f:
                    sql_content = f.read()
                encoding_used = "utf-8 (with replacements)"
                print(f"   ⚠️  Warning: Some characters were replaced during UTF-8 decoding")
            except Exception as e:
                raise ValueError(f"Could not read {sql_file_path} as UTF-8: {e}")
    
    if sql_content is None:
        raise ValueError(f"Could not read {sql_file_path} with any supported encoding")
    
    if encoding_used != "utf-8":
        print(f"   ⚠️  Note: File read with {encoding_used} encoding (not UTF-8)")
    
    with conn.cursor() as cur:
        # Execute the entire SQL file
        cur.execute(sql_content)
    conn.commit()
    print(f"✅ Completed {sql_file_path}")


def main():
    # Get the project root directory (parent of app/)
    # Use resolve() to get absolute paths for better cross-platform compatibility
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent
    db_dir = project_root / "db"
    
    schema_file = db_dir / "schema.sql"
    sample_data_file = db_dir / "sample_data.sql"
    
    # Resolve paths to absolute for better error messages
    schema_file = schema_file.resolve()
    sample_data_file = sample_data_file.resolve()
    
    # Check if files exist
    if not schema_file.exists():
        print(f"❌ Error: {schema_file} not found!")
        print(f"   Current working directory: {os.getcwd()}")
        print(f"   Script location: {script_path}")
        print(f"   Project root: {project_root}")
        return
    
    if not sample_data_file.exists():
        print(f"❌ Error: {sample_data_file} not found!")
        print(f"   Current working directory: {os.getcwd()}")
        print(f"   Script location: {script_path}")
        print(f"   Project root: {project_root}")
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
    except UnicodeDecodeError as e:
        print(f"❌ Encoding error: Could not decode SQL file with UTF-8")
        print(f"   Error details: {e}")
        print(f"\n   💡 Troubleshooting steps:")
        print(f"   1. If using VS Code:")
        print(f"      - Check bottom-right corner for file encoding")
        print(f"      - Click encoding → 'Save with Encoding' → 'UTF-8'")
        print(f"      - The .vscode/settings.json file should ensure UTF-8 encoding")
        print(f"   2. Re-save the SQL files with UTF-8 encoding (without BOM)")
        print(f"   3. Check if files contain non-UTF-8 characters")
        
        # Try to detect actual encoding for helpful error message
        try:
            # Determine which file failed by checking the error context
            failed_file = schema_file if schema_file.exists() else sample_data_file
            detected_encoding, confidence = detect_file_encoding(failed_file)
            if detected_encoding:
                print(f"\n   🔍 Detected encoding: {detected_encoding} (confidence: {confidence:.2%})")
        except (ImportError, Exception):
            pass  # Detection not available or failed
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print(f"   Please check that the SQL files exist in the db/ directory")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()




