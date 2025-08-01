#!/usr/bin/env python3
"""
Verification script for training plans API
Run this after starting the server with: uvicorn main:app --reload
"""

import requests
import json

def verify_api():
    base_url = "http://localhost:8000"
    
    print("🔍 Verifying Training Plans API...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server is running: {response.json()}")
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return
    
    # Test 2: Check OpenAPI documentation
    try:
        response = requests.get(f"{base_url}/openapi.json")
        data = response.json()
        
        # Find training-plans endpoints
        training_plans_paths = [path for path in data['paths'].keys() if 'training-plans' in path]
        print(f"\n📋 Found {len(training_plans_paths)} training-plans endpoints:")
        for path in training_plans_paths:
            methods = list(data['paths'][path].keys())
            print(f"   • {path} - Methods: {', '.join(methods)}")
        
        # Find auth endpoints
        auth_paths = [path for path in data['paths'].keys() if 'auth' in path]
        print(f"\n🔐 Found {len(auth_paths)} auth endpoints:")
        for path in auth_paths:
            methods = list(data['paths'][path].keys())
            print(f"   • {path} - Methods: {', '.join(methods)}")
            
    except Exception as e:
        print(f"❌ Error accessing OpenAPI: {e}")
    
    # Test 3: Test training plans status (should require auth)
    try:
        response = requests.get(f"{base_url}/training-plans/status")
        print("\n❌ Training plans status should require auth but didn't")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("\n✅ Training plans status correctly requires authentication")
        else:
            print(f"\n❌ Unexpected error: {e.response.status_code}")
    except Exception as e:
        print(f"\n❌ Training plans status error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 If you see the training-plans endpoints above, they're working!")
    print("📖 Visit http://localhost:8000/docs to see the Swagger UI")
    print("🔗 Visit http://localhost:8000/redoc for ReDoc documentation")

if __name__ == "__main__":
    verify_api() 