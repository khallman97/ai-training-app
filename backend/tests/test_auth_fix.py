#!/usr/bin/env python3
"""
Test script to verify the authentication fix
"""

import requests
import json

def test_auth_fix():
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Authentication Fix...")
    print("=" * 50)
    
    # Test 1: Create a test user
    print("\n1. Creating test user...")
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/signup", json=user_data)
        print(f"Signup Status: {response.status_code}")
        if response.status_code == 201:
            print("✅ User created successfully")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Login to get token
    print("\n2. Logging in to get token...")
    try:
        response = requests.post(f"{base_url}/auth/login", json=user_data)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("✅ Login successful, got token")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Response: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 3: Test training plan status with proper auth
    print("\n3. Testing training plan status with auth...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{base_url}/training-plans/status", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Authentication working!")
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Test without auth (should fail)
    print("\n4. Testing without auth (should fail)...")
    try:
        response = requests.get(f"{base_url}/training-plans/status")
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly requires authentication")
        else:
            print(f"❌ Should have failed with 401, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication fix test completed!")

if __name__ == "__main__":
    test_auth_fix() 