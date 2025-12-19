import sys
import os
from jose import jwt, JWTError

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

def debug_auth():
    print("--- Auth Debugger ---")
    print(f"Secret Key Loaded: '{settings.SECRET_KEY}' (First 5 chars: {settings.SECRET_KEY[:5]})")
    print(f"Algorithm: {settings.ALGORITHM}")
    
    token = input("\nPaste your Bearer Token here (just the token, no 'Bearer ' prefix): ").strip()
    
    # Remove quotes if user accidentally copied them from localstorage
    if token.startswith('"') and token.endswith('"'):
        token = token[1:-1]
        print("Note: Removed surrounding quotes from token.")
        
    print(f"\nDecoding token: {token[:10]}... (Length: {len(token)})")
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        print("\n[SUCCESS] Token Valid!")
        print("Payload:", payload)
        
        # Check Expiration manually to be sure
        import datetime
        if 'exp' in payload:
            exp = datetime.datetime.fromtimestamp(payload['exp'])
            now = datetime.datetime.now()
            print(f"Expires at: {exp}")
            print(f"Current time: {now}")
            if now > exp:
                print("[WARN] Token is EXPIRED according to system time!")
            else:
                print("[OK] Token is active.")
        
    except JWTError as e:
        print(f"\n[FAIL] Decode Error: {e}")
    except Exception as e:
         print(f"\n[FAIL] Unexpected Error: {e}")

if __name__ == "__main__":
    debug_auth()
