#!/usr/bin/env python3
"""
Cleanup script to remove quick fix files since we're using proper migrations
"""

import os

def cleanup_quick_fixes():
    """Remove quick fix files that are no longer needed"""
    
    # Files to remove (quick fixes that are no longer needed)
    quick_fix_files = [
        "fix_database.py",
        "docker_fix_db.py",
        "quick_fix.py"
    ]
    
    print("🧹 Cleaning up quick fix files...")
    print("These files are no longer needed since we're using proper Alembic migrations.")
    
    removed_files = []
    for file in quick_fix_files:
        if os.path.exists(file):
            os.remove(file)
            removed_files.append(file)
            print(f"✅ Removed: {file}")
        else:
            print(f"ℹ️  File not found: {file}")
    
    if removed_files:
        print(f"\n✅ Removed {len(removed_files)} quick fix files.")
    else:
        print("\nℹ️  No quick fix files found to remove.")
    
    print("\n🎉 From now on, use proper migrations:")
    print("📋 For Docker: python scripts/docker_migrate.py <command>")
    print("📋 For local: python scripts/manage_migrations.py <command>")
    print("\nAvailable commands:")
    print("  init      - Initialize database with current models")
    print("  migrate   - Create new migration from model changes")
    print("  upgrade   - Apply pending migrations")
    print("  status    - Show migration status")

if __name__ == "__main__":
    cleanup_quick_fixes() 