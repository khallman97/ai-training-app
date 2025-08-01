#!/usr/bin/env python3
"""
Test script for training plans API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_training_plans_api():
    print("Testing Training Plans API...")
    
    # Test 1: Check status without auth (should fail)
    print("\n1. Testing /training-plans/status without auth...")
    try:
        response = requests.get(f"{BASE_URL}/training-plans/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Create a user first
    print("\n2. Creating a test user...")
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=user_data)
        print(f"Signup Status: {response.status_code}")
        if response.status_code == 201:
            print("User created successfully")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Login to get token
    print("\n3. Logging in to get token...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=user_data)
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("Login successful, got token")
        else:
            print(f"Response: {response.json()}")
            return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Test 4: Check training plan status (should return no plan)
    print("\n4. Checking training plan status...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/training-plans/status", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 5: Create a training plan
    print("\n5. Creating a training plan...")
    plan_data = {
        "name": "Beginner Triathlon Plan",
        "description": "A 12-week plan for beginners",
        "plan_type": "beginner",
        "duration_weeks": 12
    }
    
    try:
        response = requests.post(f"{BASE_URL}/training-plans/", json=plan_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            plan = response.json()
            print(f"Plan created: {json.dumps(plan, indent=2)}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 6: Check status again (should return the plan)
    print("\n6. Checking training plan status again...")
    try:
        response = requests.get(f"{BASE_URL}/training-plans/status", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 7: Get all training plans
    print("\n7. Getting all training plans...")
    try:
        response = requests.get(f"{BASE_URL}/training-plans/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_training_plans_api() 