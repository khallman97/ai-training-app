#!/usr/bin/env python3
"""
Test script for the new training plan structure
"""

import requests
import json
from datetime import date, timedelta

def test_new_training_plan():
    base_url = "http://localhost:8000"
    
    print("🔍 Testing New Training Plan Structure...")
    print("=" * 60)
    
    # Test 1: Login
    print("\n1. Logging in...")
    login_data = {
        "email": "kyle123@gmail.com",
        "password": "123456789"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"✅ Got token: {token[:30]}...")
        else:
            print(f"❌ Login failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Create a new training plan with all fields
    print("\n2. Creating new training plan...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Calculate dates
    today = date.today()
    start_date = today + timedelta(days=7)  # Start next week
    event_date = start_date + timedelta(weeks=12)  # 12 weeks later
    
    training_plan_data = {
        "name": "Advanced Triathlon Plan",
        "description": "A comprehensive 12-week triathlon training plan for advanced athletes",
        "type": "Triathlon",
        "start_date": start_date.isoformat(),
        "event_date": event_date.isoformat(),
        "skill_level": "master",
        "long_days": ["saturday", "sunday"],
        "running_threshold_pace": "4:30 per km",
        "biking_fpt": 280,
        "critical_swim_speed": "1:45 per 100m"
    }
    
    try:
        response = requests.post(
            f"{base_url}/training-plans/", 
            json=training_plan_data, 
            headers=headers
        )
        print(f"Create Status: {response.status_code}")
        
        if response.status_code == 201:
            plan = response.json()
            print("✅ Training plan created successfully!")
            print(f"Plan ID: {plan['id']}")
            print(f"Type: {plan['type']}")
            print(f"Skill Level: {plan['skill_level']}")
            print(f"Long Days: {plan['long_days']}")
            print(f"Running Pace: {plan['running_threshold_pace']}")
            print(f"Biking FPT: {plan['biking_fpt']}")
            print(f"Swim Speed: {plan['critical_swim_speed']}")
        else:
            print(f"❌ Failed to create plan: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Check training plan status
    print("\n3. Checking training plan status...")
    try:
        response = requests.get(f"{base_url}/training-plans/status", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Status check successful!")
            print(f"Has Plan: {data['has_plan']}")
            if data['has_plan']:
                plan = data['plan']
                print(f"Active Plan: {plan['name']} ({plan['type']})")
        else:
            print(f"❌ Status check failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Test validation - invalid type
    print("\n4. Testing validation - invalid type...")
    invalid_plan_data = {
        "name": "Invalid Plan",
        "type": "InvalidType",  # Invalid type
        "start_date": start_date.isoformat(),
        "event_date": event_date.isoformat(),
        "skill_level": "beginner",
        "long_days": ["monday"]
    }
    
    try:
        response = requests.post(
            f"{base_url}/training-plans/", 
            json=invalid_plan_data, 
            headers=headers
        )
        print(f"Validation Status: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Validation working correctly - rejected invalid type")
        else:
            print(f"❌ Validation failed - should have rejected invalid type: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 New training plan structure test completed!")

if __name__ == "__main__":
    test_new_training_plan() 