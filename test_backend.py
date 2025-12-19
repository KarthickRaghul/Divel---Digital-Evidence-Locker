import requests
import os

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_flow():
    print("🚀 Starting Backend Verification...")
    
    # 1. Login as Polaris
    print("\n🔐 Logging in as Polaris...")
    payload = {"username": "polaris", "password": "polaris123"}
    response = requests.post(f"{BASE_URL}/auth/login", data=payload)
    if response.status_code != 200:
        print(f"❌ Login Failed: {response.text}")
        return
    token = response.json()["access_token"]
    print("✅ Polaris Logged In")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Upload Evidence
    print("\n📤 Uploading Evidence (test.txt)...")
    with open("test.txt", "w") as f:
        f.write("This is a piece of digital-evidence")
    
    files = {'file': open('test.txt', 'rb')}
    data = {'case_id': 'CASE-2025-001'}
    
    response = requests.post(f"{BASE_URL}/evidence/upload", headers=headers, files=files, data=data)
    if response.status_code != 200:
         print(f"❌ Upload Failed: {response.text}")
         return

    evidence_data = response.json()
    evidence_id = evidence_data["evidence_id"]
    print(f"✅ Upload Success! ID: {evidence_id}")
    print(f"   Hash: {evidence_data['hash']}")
    print(f"   Tx: {evidence_data['tx_hash']}")
    
    # 3. Verify as Forensics
    print("\n🔍 Verifying as Forensics...")
    # Login as Forensics
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": "forensics", "password": "forensics123"})
    forensics_token = response.json()["access_token"]
    forensics_headers = {"Authorization": f"Bearer {forensics_token}"}
    
    verify_response = requests.get(f"{BASE_URL}/evidence/{evidence_id}/verify", headers=forensics_headers)
    if verify_response.status_code == 200:
        result = verify_response.json()
        print(f"✅ Verification Result: {result['status']}")
    else:
        print(f"❌ Verification Failed: {verify_response.text}")

    # 4. Clean up
    os.remove("test.txt")
    print("\n🎉 Verification Complete!")

if __name__ == "__main__":
    test_flow()
