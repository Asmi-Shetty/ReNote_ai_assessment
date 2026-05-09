import requests
import uuid

username = f"test_{uuid.uuid4().hex[:6]}"
# 0. Register
requests.post("http://127.0.0.1:8000/auth/register", json={"username": username, "email": f"{username}@example.com", "password": "password"})

# 1. Login to get token
login_res = requests.post("http://127.0.0.1:8000/auth/login", data={"username": f"{username}@example.com", "password": "password"})
token = login_res.json().get("access_token")
print("Token:", token)

# 2. Upload file
headers = {
    "X-Description": "test desc",
    "Authorization": f"Bearer {token}"
}
files = {"file": ("test.txt", b"test content", "text/plain")}
res = requests.post("http://127.0.0.1:8000/rag/documents/upload", headers=headers, files=files)
print(res.status_code, res.text)
