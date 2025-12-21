from app.core.config import settings
import openai
import json
from docling.document_converter import DocumentConverter

class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        # Lazy load converter to avoid startup issues if not used immediately
        self._converter = None
        if self.api_key:
            openai.api_key = self.api_key

    @property
    def converter(self):
        if self._converter is None:
            self._converter = DocumentConverter()
        return self._converter

    def _convert_file_to_markdown(self, file_path: str) -> str:
        """Uses Docling to convert PDF/Image to Markdown."""
        try:
            result = self.converter.convert(file_path)
            return result.document.export_to_markdown()
        except Exception as e:
            print(f"Docling conversion error: {e}")
            return f"Error parsing document: {str(e)}"

    def _run_detective_agent(self, text_content: str) -> str:
        """Detective Agent: Generates a professional police case summary."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a senior forensic detective. Read the provided evidence text and write a professional, concise case summary. Focus on facts, dates, and key individuals. Do not use markdown formatting, just plain text."},
                    {"role": "user", "content": text_content[:10000]} # Truncate to avoid token limits
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def _run_analyst_agent(self, text_content: str) -> dict:
        """Analyst Agent: Extracts entities and relationships for Knowledge Graph."""
        try:
            prompt = """
            You are a Crime Analyst. Extract entities and relationships from the text for a Knowledge Graph.
            Return ONLY valid JSON in this format:
            {
                "nodes": [{"id": "Name", "group": "Person|Location|Incident|Evidence"}],
                "links": [{"source": "Name", "target": "Name", "value": "relationship description"}]
            }
            Ensure 'source' and 'target' IDs exist in 'nodes'.
            """
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text_content[:10000]}
                ]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Analyst Agent error: {e}")
            return {"nodes": [], "links": []}

    def generate_summary(self, file_path: str) -> dict:
        if not self.api_key:
             return {
                "summary": "AI Service not configured (Missing API Key)",
                "graph": {"nodes": [], "links": []}
            }
        
        # 1. Parse Document via Docling
        markdown_content = self._convert_file_to_markdown(file_path)
        
        # 2. Run Agents
        summary = self._run_detective_agent(markdown_content)
        graph_data = self._run_analyst_agent(markdown_content)
        
        return {
            "summary": summary,
            "graph": graph_data
        }

ai_service = AIService()
