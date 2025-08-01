#!/usr/bin/env python3
"""
Quick Fix Script - Directly update database schema
This script will create the missing columns in your training_plans table
"""

import psycopg2
import sys
from datetime import datetime

def connect_to_db():
    """Connect to the database"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="ai_training_app",
            user="aiuser",
            password="aipassword"
        )
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def check_table_exists(conn, table_name):
    """Check if a table exists"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        );
    """, (table_name,))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists

def check_column_exists(conn, table_name, column_name):
    """Check if a column exists in a table"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.columns 
            WHERE table_name = %s AND column_name = %s
        );
    """, (table_name, column_name))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists

def add_column(conn, table_name, column_name, column_type):
    """Add a column to a table"""
    cursor = conn.cursor()
    try:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
        conn.commit()
        print(f"✅ Added column {column_name} to {table_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to add column {column_name}: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()

def main():
    print("🔧 Quick Database Schema Fix")
    print("This script will add missing columns to your training_plans table")
    
    # Connect to database
    conn = connect_to_db()
    if not conn:
        print("❌ Cannot connect to database. Make sure:")
        print("1. Your database is running")
        print("2. You're using the correct connection details")
        return
    
    # Check if training_plans table exists
    if not check_table_exists(conn, "training_plans"):
        print("❌ training_plans table doesn't exist!")
        print("Please run your application first to create the tables.")
        conn.close()
        return
    
    print("✅ training_plans table exists")
    
    # Define the new columns we need to add
    new_columns = [
        ("type", "VARCHAR"),
        ("start_date", "DATE"),
        ("event_date", "DATE"),
        ("skill_level", "VARCHAR"),
        ("long_days", "JSONB"),
        ("running_threshold_pace", "VARCHAR"),
        ("biking_fpt", "INTEGER"),
        ("critical_swim_speed", "VARCHAR"),
        ("additional_data", "JSONB")
    ]
    
    # Check and add missing columns
    added_columns = []
    for column_name, column_type in new_columns:
        if not check_column_exists(conn, "training_plans", column_name):
            if add_column(conn, "training_plans", column_name, column_type):
                added_columns.append(column_name)
        else:
            print(f"ℹ️  Column {column_name} already exists")
    
    conn.close()
    
    if added_columns:
        print(f"\n✅ Successfully added {len(added_columns)} columns:")
        for col in added_columns:
            print(f"   - {col}")
        print("\n🎉 Your database schema is now up to date!")
    else:
        print("\n✅ All required columns already exist!")
    
    print("\nYou can now restart your application and it should work properly.")

if __name__ == "__main__":
    main() 