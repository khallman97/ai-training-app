#!/usr/bin/env python3
"""
Debug test to see what's causing import issues
"""

print("Starting debug test...")

try:
    print("1. Testing basic imports...")
    import fastapi
    print("✅ FastAPI imported")
    
    import sqlalchemy
    print("✅ SQLAlchemy imported")
    
    import pydantic
    print("✅ Pydantic imported")
    
except Exception as e:
    print(f"❌ Import error: {e}")

try:
    print("\n2. Testing auth module...")
    from auth import router as auth_router
    print("✅ Auth router imported")
except Exception as e:
    print(f"❌ Auth import error: {e}")

try:
    print("\n3. Testing training_plans module...")
    from training_plans import router as training_plans_router
    print("✅ Training plans router imported")
except Exception as e:
    print(f"❌ Training plans import error: {e}")

try:
    print("\n4. Testing main module...")
    from main import app
    print("✅ Main app imported")
except Exception as e:
    print(f"❌ Main import error: {e}")

print("\nDebug test completed!") 