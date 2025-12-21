import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from app.services.ai import ai_service
    print("✅ AI Service imported successfully.")
    
    if ai_service.api_key:
        print("✅ OpenAI API Key detected.")
    else:
        print("⚠️ OpenAI API Key NOT detected (Check .env).")

    # Check method signatures
    if hasattr(ai_service, 'generate_summary'):
         print("✅ generate_summary method exists.")
    else:
         print("❌ generate_summary method MISSING.")

    print("AI Service Verification Complete.")
    
except Exception as e:
    print(f"❌ Verification Failed: {e}")
