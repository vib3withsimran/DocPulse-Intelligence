from groq import Groq
import json
import os

class DocumentClassifier:
    def __init__(self, api_key: str = None):
        # Load the key passed in, or default to the GROQ_API_KEY environment variable
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
    
    def classify(self, text: str, filename: str) -> dict:
        """Classify document using LLM"""
        # If API key is missing, return the fallback dictionary immediately
        if not self.api_key:
            return {
                "document_type": "other",
                "sensitivity": "internal",
                "has_tables": False,
                "topics": ["unknown"],
                "language": "english",
                "error": "Groq API key not configured"
            }
            
        # Take only first 2000 chars (faster, cheaper)
        sample = text[:2000]
        
        prompt = f"""Analyze this document and return ONLY valid JSON.

Filename: {filename}
Content: {sample}

Return JSON in this exact format:
{{
    "document_type": "invoice" OR "contract" OR "report" OR "handwritten" OR "other",
    "sensitivity": "public" OR "internal" OR "confidential",
    "has_tables": true OR false,
    "topics": ["topic1", "topic2"],
    "language": "english" OR "other"
}}

JSON:"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.2-3b-preview",  # Fast and free
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1  # Lower = more consistent
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content.strip()
            
            # Simple sanitization to extract JSON block if the LLM includes conversational formatting
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            result = json.loads(content)
            return result
            
        except Exception as e:
            # Fallback if LLM fails or returns malformed JSON
            return {
                "document_type": "other",
                "sensitivity": "internal",
                "has_tables": False,
                "topics": ["unknown"],
                "language": "english",
                "error": str(e)
            }
