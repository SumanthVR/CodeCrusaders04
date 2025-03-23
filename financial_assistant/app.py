from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS  # 🚀 Import Flask-CORS
from models.gemini_service import GeminiService
from models.financial_data import FinancialDataService
from utils.helpers import format_response, validate_input
from utils.prompts import get_financial_prompt

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# 🚀 Enable CORS for frontend requests
CORS(app)  

# Initialize services
gemini_service = GeminiService(api_key=os.getenv("GOOGLE_API_KEY"))
financial_data = FinancialDataService()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat request and return AI response"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Validate user input
        if not validate_input(user_message):
            return jsonify({'response': 'Please enter a valid financial question or query.'})
        
        # Check if we need financial data for this query
        if financial_data.needs_market_data(user_message):
            market_context = financial_data.get_relevant_data(user_message)
            prompt = get_financial_prompt(user_message, market_context)
        else:
            prompt = get_financial_prompt(user_message)
        
        # Get response from Gemini
        response = gemini_service.generate_response(prompt)
        formatted_response = format_response(response)
        
        return jsonify({'response': formatted_response})
        
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({'response': 'Sorry, I encountered an error. Please try again later.'}), 500

@app.route('/search-investments', methods=['POST'])
def search_investments():
    """Search for investment products based on criteria"""
    try:
        data = request.json
        criteria = data.get('criteria', {})
        
        # Get investment recommendations
        results = financial_data.search_investments(criteria)
        
        return jsonify({'results': results})
        
    except Exception as e:
        app.logger.error(f"Error searching investments: {str(e)}")
        return jsonify({'error': 'Failed to search for investments'}), 500

if __name__ == '__main__':
    app.run(debug=os.getenv("FLASK_ENV") == "development")
