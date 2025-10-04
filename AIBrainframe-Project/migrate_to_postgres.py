#!/usr/bin/env python3
"""
Database migration script for AIBrainFrame project
This script helps migrate from SQLite to PostgreSQL and validates the setup.
"""

import os
import sys
import sqlite3
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from decouple import config
from app.models import Base

def test_sqlite_connection():
    """Test SQLite connection and show current data"""
    print("Testing SQLite connection...")

    try:
        sqlite_url = "sqlite:///./aibrainframe.db"
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

        with engine.connect() as conn:
            # Check if tables exist
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]

            print(f"✓ SQLite connection successful")
            print(f"Tables found: {len(tables)}")

            if tables:
                for table in tables:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"  - {table}: {count} records")

            return True, tables

    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False, []

def test_postgres_connection():
    """Test PostgreSQL connection"""
    print("\nTesting PostgreSQL connection...")

    db_host = config('DB_HOST', default='localhost')
    db_name = config('DB_NAME', default='aibrainframe_db')
    db_user = config('DB_USER', default='aibrainframe_user')
    db_password = config('DB_PASSWORD', default='0320')

    try:
        postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
        engine = create_engine(postgres_url)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ PostgreSQL connection successful")
            print(f"Version: {version}")

            # Check existing tables
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"Existing tables: {len(tables)}")

            return True, tables

    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("This is expected if the database hasn't been set up yet.")
        return False, []

def create_postgres_schema():
    """Create the schema in PostgreSQL using SQLAlchemy models"""
    print("\nCreating PostgreSQL schema...")

    db_host = config('DB_HOST', default='localhost')
    db_name = config('DB_NAME', default='aibrainframe_db')
    db_user = config('DB_USER', default='aibrainframe_user')
    db_password = config('DB_PASSWORD', default='0320')

    try:
        postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
        engine = create_engine(postgres_url)

        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✓ PostgreSQL schema created successfully")

        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"Tables created: {len(tables)}")
            for table in sorted(tables):
                print(f"  - {table}")

        return True

    except Exception as e:
        print(f"❌ Failed to create PostgreSQL schema: {e}")
        return False

def export_sqlite_data():
    """Export data from SQLite for manual migration"""
    print("\nExporting SQLite data...")

    try:
        conn = sqlite3.connect('./aibrainframe.db')
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        export_data = {}
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            export_data[table] = {
                'columns': columns,
                'rows': rows
            }
            print(f"  - Exported {table}: {len(rows)} records")

        conn.close()

        # Save export info
        with open('sqlite_export_summary.txt', 'w') as f:
            f.write("SQLite Data Export Summary\n")
            f.write("=" * 50 + "\n\n")
            for table, data in export_data.items():
                f.write(f"Table: {table}\n")
                f.write(f"Columns: {', '.join(data['columns'])}\n")
                f.write(f"Records: {len(data['rows'])}\n\n")

        print("✓ Export summary saved to sqlite_export_summary.txt")
        return export_data

    except Exception as e:
        print(f"❌ Failed to export SQLite data: {e}")
        return {}

def create_postgres_setup_instructions():
    """Create setup instructions for PostgreSQL"""

    db_name = config('DB_NAME', default='aibrainframe_db')
    db_user = config('DB_USER', default='aibrainframe_user')
    db_password = config('DB_PASSWORD', default='0320')

    instructions = f"""
PostgreSQL Setup Instructions for AIBrainFrame
==============================================

Since automatic setup requires elevated privileges, here are manual setup instructions:

1. Connect to PostgreSQL as superuser:
   sudo -u postgres psql

2. Create the database:
   CREATE DATABASE {db_name};

3. Create the user:
   CREATE USER {db_user} WITH PASSWORD '{db_password}';

4. Grant privileges:
   GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};

   -- For PostgreSQL 15+ you may also need:
   GRANT ALL ON SCHEMA public TO {db_user};

5. Exit PostgreSQL:
   \\q

6. Test the connection:
   psql -h localhost -U {db_user} -d {db_name}

7. Update your .env file to enable PostgreSQL:
   USE_POSTGRES=true

8. Run the migration script again to create the schema:
   python migrate_to_postgres.py

Alternative: Using createdb and createuser commands:
   sudo -u postgres createdb {db_name}
   sudo -u postgres createuser -P {db_user}
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"

Environment Configuration:
- DB_HOST=localhost
- DB_NAME={db_name}
- DB_USER={db_user}
- DB_PASSWORD={db_password}
- USE_POSTGRES=true
"""

    with open('postgres_setup_instructions.txt', 'w') as f:
        f.write(instructions)

    print("✓ Setup instructions saved to postgres_setup_instructions.txt")
    return instructions

def main():
    """Main migration function"""
    print("AIBrainFrame Database Migration Tool")
    print("=" * 50)

    # Test current SQLite setup
    sqlite_ok, sqlite_tables = test_sqlite_connection()

    # Test PostgreSQL connection
    postgres_ok, postgres_tables = test_postgres_connection()

    if not postgres_ok:
        print("\nPostgreSQL is not accessible. Creating setup instructions...")
        create_postgres_setup_instructions()

        if sqlite_ok and sqlite_tables:
            print("\nExporting SQLite data for manual migration...")
            export_sqlite_data()

        print("\n" + "=" * 50)
        print("NEXT STEPS:")
        print("1. Follow the instructions in postgres_setup_instructions.txt")
        print("2. Set USE_POSTGRES=true in your .env file")
        print("3. Run this script again to create the schema")
        print("4. Restart your FastAPI application")

    else:
        print("\nPostgreSQL is accessible! Creating schema...")
        if create_postgres_schema():
            print("\n🎉 PostgreSQL setup completed successfully!")
            print("You can now set USE_POSTGRES=true in your .env file")
        else:
            print("\n❌ Schema creation failed")

if __name__ == "__main__":
    main()