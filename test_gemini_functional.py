import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from app.services.ai import ai_service
    
    print("🚀 Starting Functional Test...")
    
    if not ai_service.api_key:
        print("❌ SKIPPING: No API Key found.")
        sys.exit(1)

    # Test Detective Agent (Simple Text Generation)
    print("🔎 Testing Detective Agent...")
    summary = ai_service._run_detective_agent("This is a test case. Suspect John Doe was seen at the park at 10 PM stealing a cookie.")
    print(f"📝 Summary Result: {summary[:100]}...") # Print first 100 chars
    
    if "Error" in summary or "Gemini Client not initialized" in summary:
        print("❌ Detective Agent Failed.")
    else:
        print("✅ Detective Agent Worked!")

    # Test Analyst Agent (JSON Generation)
    print("🕸️ Testing Analyst Agent...")
    graph = ai_service._run_analyst_agent("John Doe lives in New York.")
    print(f"📊 Graph Result: {graph}")
    
    if graph.get("nodes"):
        print("✅ Analyst Agent Worked!")
    else:
        print("⚠️ Analyst Agent returned empty graph (might be expected for short text) or failed.")

except Exception as e:
    print(f"❌ functional Test Failed: {e}")
