from app.core.config import settings
import openai

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if self.api_key:
            openai.api_key = self.api_key

    def generate_summary(self, evidence_text_content: str) -> dict:
        if not self.api_key:
             return {
                "summary": "AI Service not configured (Missing API Key)",
                "keywords": []
            }
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a forensic assistant. Summarize the following evidence text and extract key entities."},
                    {"role": "user", "content": evidence_text_content}
                ]
            )
            content = response.choices[0].message.content
            return {
                "summary": content,
                "keywords": ["extracted", "from", "ai"] # fast placeholder
            }
        except Exception as e:
            return {"error": str(e)}

ai_service = AIService()
