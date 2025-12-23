import requests
import json

try:
    response = requests.get('http://localhost:8000/api/v1/cases/')
    response.raise_for_status()
    data = response.json()
    print("Status Code:", response.status_code)
    print("Number of cases:", len(data))
    if len(data) > 0:
        print("First case sample:")
        print(json.dumps(data[0], indent=2))
        print("\nKeys in first case:", data[0].keys())
    else:
        print("No cases found.")
except Exception as e:
    print(f"Error: {e}")
