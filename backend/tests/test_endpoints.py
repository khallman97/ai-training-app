#!/usr/bin/env python3
"""
Simple test to verify training plans endpoints are accessible
"""

import urllib.request
import json

def test_endpoints():
    base_url = "http://localhost:8000"
    
    print("Testing API endpoints...")
    
    # Test 1: Root endpoint
    try:
        response = urllib.request.urlopen(f"{base_url}/")
        data = response.read().decode()
        print(f"✓ Root endpoint: {data}")
    except Exception as e:
        print(f"✗ Root endpoint error: {e}")
    
    # Test 2: OpenAPI JSON
    try:
        response = urllib.request.urlopen(f"{base_url}/openapi.json")
        data = json.loads(response.read().decode())
        
        # Check for training-plans endpoints
        training_plans_paths = [path for path in data['paths'].keys() if 'training-plans' in path]
        print(f"✓ Found {len(training_plans_paths)} training-plans endpoints:")
        for path in training_plans_paths:
            print(f"  - {path}")
            
        # Check for auth endpoints
        auth_paths = [path for path in data['paths'].keys() if 'auth' in path]
        print(f"✓ Found {len(auth_paths)} auth endpoints:")
        for path in auth_paths:
            print(f"  - {path}")
            
    except Exception as e:
        print(f"✗ OpenAPI JSON error: {e}")
    
    # Test 3: Training plans status (should require auth)
    try:
        response = urllib.request.urlopen(f"{base_url}/training-plans/status")
        print("✗ Training plans status should require auth but didn't")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("✓ Training plans status correctly requires authentication")
        else:
            print(f"✗ Unexpected error: {e.code}")
    except Exception as e:
        print(f"✗ Training plans status error: {e}")

if __name__ == "__main__":
    test_endpoints() 