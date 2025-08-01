#!/usr/bin/env python3
"""
Simple test to verify authentication is working
"""

import requests
import json

def test_simple():
    base_url = "http://localhost:8000"
    
    print("🔍 Simple Authentication Test...")
    
    # Test 1: Login
    print("\n1. Logging in...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"✅ Got token: {token[:30]}...")
            
            # Test 2: Use token
            print("\n2. Testing with token...")
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.get(f"{base_url}/training-plans/status", headers=headers)
            print(f"Status endpoint: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Response: {json.dumps(data, indent=2)}")
            else:
                print(f"❌ Failed: {response.text}")
                
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple() 