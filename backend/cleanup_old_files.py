#!/usr/bin/env python3
"""
Cleanup script to remove old files after reorganization
"""

import os
import shutil

def cleanup_old_files():
    """Remove old files that have been reorganized"""
    
    # Files to remove (they've been moved to new locations)
    old_files = [
        "auth.py",
        "training_plans.py", 
        "main.py",
        "security.py",
        "quick_fix.py",
        "docker_migrate.py",
        "direct_migrate.py",
        "setup_migrations.py",
        "manage_migrations.py",
        "MIGRATIONS_README.md",
        "README_TRAINING_PLANS.md"
    ]
    
    # Test files to move to tests directory
    test_files = [
        "test_new_training_plan.py",
        "test_training_plans.py",
        "test_auth_fix.py",
        "test_tags.py",
        "test_endpoints.py",
        "verify_api.py",
        "simple_test.py",
        "debug_test.py"
    ]
    
    print("🧹 Cleaning up old files...")
    
    # Remove old files
    for file in old_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"✅ Removed: {file}")
        else:
            print(f"ℹ️  File not found: {file}")
    
    # Move test files to tests directory
    if not os.path.exists("tests"):
        os.makedirs("tests")
    
    for file in test_files:
        if os.path.exists(file):
            shutil.move(file, f"tests/{file}")
            print(f"✅ Moved: {file} -> tests/{file}")
        else:
            print(f"ℹ️  File not found: {file}")
    
    print("\n🎉 Cleanup completed!")
    print("\nYour backend is now organized with the new structure:")
    print("📁 app/ - Main application code")
    print("📁 scripts/ - Utility scripts")
    print("📁 tests/ - Test files")
    print("📁 docs/ - Documentation")
    print("📁 migrations/ - Database migrations")

if __name__ == "__main__":
    cleanup_old_files() 