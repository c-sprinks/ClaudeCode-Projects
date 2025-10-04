#!/usr/bin/env python3
"""
PostgreSQL setup script for AIBrainFrame project
This script attempts to create the database and user for the project.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from decouple import config

def setup_postgres():
    """Setup PostgreSQL database and user for AIBrainFrame"""

    # Database configuration from environment
    db_host = config('DB_HOST', default='localhost')
    db_name = config('DB_NAME', default='aibrainframe_db')
    db_user = config('DB_USER', default='aibrainframe_user')
    db_password = config('DB_PASSWORD', default='0320')

    print(f"Setting up PostgreSQL database: {db_name}")
    print(f"Database host: {db_host}")
    print(f"Database user: {db_user}")

    # Connection options to try
    connection_options = [
        # Try with current user (peer authentication)
        {'host': db_host, 'user': os.getenv('USER'), 'database': 'postgres'},
        # Try with postgres user (if available)
        {'host': db_host, 'user': 'postgres', 'database': 'postgres'},
        # Try with default local connection
        {'database': 'postgres'},
    ]

    conn = None
    for i, conn_params in enumerate(connection_options, 1):
        try:
            print(f"\nAttempt {i}: Trying connection with {conn_params}")
            conn = psycopg2.connect(**conn_params)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            print("✓ Connected to PostgreSQL successfully!")
            break
        except psycopg2.Error as e:
            print(f"✗ Connection attempt {i} failed: {e}")
            continue

    if not conn:
        print("\n❌ Could not connect to PostgreSQL with any method.")
        print("Please ensure PostgreSQL is running and you have appropriate permissions.")
        print("\nYou can manually create the database and user with these commands:")
        print(f"sudo -u postgres createdb {db_name}")
        print(f"sudo -u postgres psql -c \"CREATE USER {db_user} WITH PASSWORD '{db_password}';\"")
        print(f"sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};\"")
        return False

    cursor = conn.cursor()

    try:
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if cursor.fetchone():
            print(f"✓ Database '{db_name}' already exists")
        else:
            # Create database
            print(f"Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✓ Database '{db_name}' created successfully")

        # Check if user exists
        cursor.execute("SELECT 1 FROM pg_user WHERE usename = %s", (db_user,))
        if cursor.fetchone():
            print(f"✓ User '{db_user}' already exists")
        else:
            # Create user
            print(f"Creating user '{db_user}'...")
            cursor.execute(f"CREATE USER \"{db_user}\" WITH PASSWORD %s", (db_password,))
            print(f"✓ User '{db_user}' created successfully")

        # Grant privileges
        print(f"Granting privileges to '{db_user}' on database '{db_name}'...")
        cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE "{db_name}" TO "{db_user}"')
        print(f"✓ Privileges granted successfully")

        print(f"\n🎉 PostgreSQL setup completed successfully!")
        print(f"Database: {db_name}")
        print(f"User: {db_user}")
        print(f"Host: {db_host}")

        return True

    except psycopg2.Error as e:
        print(f"❌ Error during setup: {e}")
        return False

    finally:
        cursor.close()
        conn.close()

def test_connection():
    """Test connection to the configured database"""

    db_host = config('DB_HOST', default='localhost')
    db_name = config('DB_NAME', default='aibrainframe_db')
    db_user = config('DB_USER', default='aibrainframe_user')
    db_password = config('DB_PASSWORD', default='0320')

    print(f"\nTesting connection to {db_name} as {db_user}...")

    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✓ Connection successful!")
        print(f"PostgreSQL version: {version}")

        cursor.close()
        conn.close()
        return True

    except psycopg2.Error as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("AIBrainFrame PostgreSQL Setup")
    print("=" * 50)

    if setup_postgres():
        test_connection()
    else:
        print("\nSetup failed. Please check the error messages above.")