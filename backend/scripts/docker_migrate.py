#!/usr/bin/env python3
"""
Docker Migration Management Script
Run this from your host machine to manage migrations in Docker
"""

import subprocess
import sys
import os

def run_docker_command(command, description):
    """Run a command inside the Docker container"""
    print(f"\n🔄 {description}...")
    print(f"Running: docker-compose exec backend {command}")
    
    try:
        result = subprocess.run(
            f"docker-compose exec backend {command}", 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
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
🐳 Docker Database Migration Management

Usage:
  python scripts/docker_migrate.py <command>

Commands:
  init          - Initialize the database with current models
  migrate       - Create a new migration from model changes
  upgrade       - Apply pending migrations to database
  downgrade     - Rollback the last migration
  status        - Show migration status
  reset         - Reset database (WARNING: This will delete all data!)
  shell         - Open a shell in the backend container
""")
        return

    command = sys.argv[1]
    
    if command == "init":
        # Create initial migration
        if run_docker_command("python scripts/manage_migrations.py init", "Creating initial migration"):
            print("✅ Database initialized successfully!")
    
    elif command == "migrate":
        # Create new migration
        message = sys.argv[2] if len(sys.argv) > 2 else "Auto-generated migration"
        run_docker_command(f'python scripts/manage_migrations.py migrate "{message}"', "Creating new migration")
    
    elif command == "upgrade":
        # Apply migrations
        run_docker_command("python scripts/manage_migrations.py upgrade", "Applying migrations")
    
    elif command == "downgrade":
        # Rollback migration
        run_docker_command("python scripts/manage_migrations.py downgrade", "Rolling back migration")
    
    elif command == "status":
        # Show status
        run_docker_command("python scripts/manage_migrations.py status", "Checking migration status")
    
    elif command == "reset":
        # Reset database (dangerous!)
        confirm = input("⚠️  WARNING: This will delete all data! Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            run_docker_command("python scripts/manage_migrations.py reset", "Resetting database")
        else:
            print("❌ Reset cancelled.")
    
    elif command == "shell":
        # Open shell in container
        print("🐳 Opening shell in backend container...")
        subprocess.run("docker-compose exec backend bash", shell=True)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments to see available commands.")

if __name__ == "__main__":
    main() 