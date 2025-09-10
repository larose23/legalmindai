#!/usr/bin/env python3
"""
Test script for LegalMind Backend deployment
Run this script to verify all endpoints are working correctly
"""

import requests
import json
import sys

def test_endpoint(base_url, endpoint, method="GET", data=None, expected_status=200):
    """Test a single endpoint"""
    url = f"{base_url}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
            
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            return True
        else:
            print(f"❌ {method} {endpoint} - Status: {response.status_code} (Expected: {expected_status})")
            print(f"   Response: {response.text[:100]}...")
            return False
    except Exception as e:
        print(f"❌ {method} {endpoint} - Error: {str(e)}")
        return False

def main():
    # Get base URL from command line argument or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = "http://localhost:5000"
    
    print(f"🧪 Testing LegalMind Backend at: {base_url}")
    print("=" * 50)
    
    # Test endpoints
    tests = [
        ("/api/legalmind/health", "GET"),
        ("/api/users", "GET"),
        ("/api/legalmind/ingest-sample-data", "POST"),
    ]
    
    # Test document analysis
    test_document = {
        "text": "This is a sample contract between Company A and Company B, effective January 1, 2024. The contract shall be governed by the laws of California."
    }
    
    passed = 0
    total = len(tests) + 1  # +1 for document analysis test
    
    for endpoint, method in tests:
        if test_endpoint(base_url, endpoint, method):
            passed += 1
    
    # Test document analysis
    if test_endpoint(base_url, "/api/legalmind/analyze-document", "POST", test_document):
        passed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your LegalMind Backend is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())