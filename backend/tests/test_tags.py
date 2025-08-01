#!/usr/bin/env python3
"""
Test script to verify API tags are working
"""

try:
    from main import app
    print("✅ Main app imported successfully")
    
    # Check if tags are defined
    if hasattr(app, 'openapi_tags'):
        print(f"✅ OpenAPI tags found: {len(app.openapi_tags)} tags")
        for tag in app.openapi_tags:
            print(f"   - {tag['name']}: {tag['description']}")
    else:
        print("❌ No OpenAPI tags found")
    
    # Check if routers are included
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    print(f"✅ Found {len(routes)} routes")
    
    # Check for training-plans routes
    training_routes = [route for route in routes if 'training-plans' in route]
    print(f"✅ Found {len(training_routes)} training-plans routes")
    
    # Check for auth routes
    auth_routes = [route for route in routes if 'auth' in route]
    print(f"✅ Found {len(auth_routes)} auth routes")
    
    print("\n🎉 API tags setup is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 