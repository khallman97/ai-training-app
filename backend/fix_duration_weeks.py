#!/usr/bin/env python3
"""
Quick fix to make duration_weeks column nullable
"""

import psycopg2
import sys

def connect_to_db():
    """Connect to the database"""
    try:
        conn = psycopg2.connect(
            host="ai-training-app-db-1",  # Use Docker service name
            port="5432",
            database="ai_training_app",
            user="aiuser",
            password="aipassword"
        )
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def fix_duration_weeks():
    """Make duration_weeks column nullable"""
    print("🔧 Fixing duration_weeks column constraint...")
    
    conn = connect_to_db()
    if not conn:
        print("❌ Cannot connect to database. Make sure:")
        print("1. Your database container is running")
        print("2. You're running this inside the backend container")
        return
    
    cursor = conn.cursor()
    
    try:
        # Check if column exists and its current constraint
        cursor.execute("""
            SELECT column_name, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'training_plans' AND column_name = 'duration_weeks';
        """)
        
        result = cursor.fetchone()
        if not result:
            print("❌ duration_weeks column not found!")
            return
        
        column_name, is_nullable = result
        print(f"ℹ️  Current duration_weeks column: nullable = {is_nullable}")
        
        if is_nullable == 'NO':
            # Make the column nullable
            cursor.execute("ALTER TABLE training_plans ALTER COLUMN duration_weeks DROP NOT NULL;")
            conn.commit()
            print("✅ Made duration_weeks column nullable")
        else:
            print("ℹ️  duration_weeks column is already nullable")
            
    except Exception as e:
        print(f"❌ Error fixing duration_weeks: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_duration_weeks() 