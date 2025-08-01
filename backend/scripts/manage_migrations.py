#!/usr/bin/env python3
"""
Database Migration Management Script
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False

def main():
    if len(sys.argv) < 2:
        print("""
🔧 Database Migration Management

Usage:
  python scripts/manage_migrations.py <command>

Commands:
  init          - Initialize the database with current models
  migrate       - Create a new migration from model changes
  upgrade       - Apply pending migrations to database
  downgrade     - Rollback the last migration
  status        - Show migration status
  reset         - Reset database (WARNING: This will delete all data!)
""")
        return

    command = sys.argv[1]
    
    if command == "init":
        # Create initial migration
        if run_command("alembic revision --autogenerate -m 'Initial migration'", "Creating initial migration"):
            run_command("alembic upgrade head", "Applying initial migration")
    
    elif command == "migrate":
        # Create new migration
        message = sys.argv[2] if len(sys.argv) > 2 else "Auto-generated migration"
        run_command(f'alembic revision --autogenerate -m "{message}"', "Creating new migration")
    
    elif command == "upgrade":
        # Apply migrations
        run_command("alembic upgrade head", "Applying migrations")
    
    elif command == "downgrade":
        # Rollback migration
        run_command("alembic downgrade -1", "Rolling back migration")
    
    elif command == "status":
        # Show status
        run_command("alembic current", "Checking current migration")
        run_command("alembic history", "Showing migration history")
    
    elif command == "reset":
        # Reset database (dangerous!)
        confirm = input("⚠️  WARNING: This will delete all data! Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            run_command("alembic downgrade base", "Rolling back all migrations")
            run_command("alembic upgrade head", "Reapplying all migrations")
        else:
            print("❌ Reset cancelled.")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments to see available commands.")

if __name__ == "__main__":
    main() 