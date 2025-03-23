"""
Service for interacting with Google's Gemini API
"""
import google.generativeai as genai
from config import GEMINI_MODEL

class GeminiService:
    """Service for interacting with Google's Gemini model"""
    
    def __init__(self, api_key):
        """Initialize the Gemini service with API key"""
        self.api_key = api_key
        self.configure_api()
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.chat_session = None
        
    def configure_api(self):
        """Configure the Gemini API with credentials"""
        genai.configure(api_key=self.api_key)
    def start_chat(self):
        """Start a new chat session"""
        self.chat_session = self.model.start_chat(
            history=[],
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "top_k": 40,
            }
        )
        return self.chat_session
    def generate_response(self, prompt):
        """Generate a response using the Gemini model"""
        try:
            if not self.chat_session:
                self.start_chat()
                
            response = self.chat_session.send_message(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I'm sorry, I'm having trouble responding right now. Please try again later."
    
    def generate_direct_response(self, prompt):
        """Generate a one-time response without chat history"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating direct response: {str(e)}")
            return "I'm sorry, I'm having trouble responding right now. Please try again later."
    
    def reset_chat(self):
        """Reset the chat session"""
        self.chat_session = None