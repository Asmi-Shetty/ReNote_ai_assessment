import requests
import json
import uuid

def test_api():
    # We need a token. Let's see if there is an endpoint to get a token or if we can mock it.
    # The auth.py router probably has a login endpoint.
    # Let's try to login as "jarvis" with password "password" based on the logs in app.log.
    
    login_data = {
        "username": "jarvis",
        "password": "password"
    }
    
    try:
        response = requests.post("http://localhost:8000/auth/login", data=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"Got token: {token}")
            
            # Now query
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            query_payload = {
                "query": "explain what all things are mentioned in the 3rd section of the pdf uploaded here",
                "session_id": str(uuid.uuid4())
            }
            
            print("Sending query...")
            q_res = requests.post("http://localhost:8000/rag/query", json=query_payload, headers=headers)
            print(f"Status Code: {q_res.status_code}")
            print(f"Response: {q_res.text}")
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
