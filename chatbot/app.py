import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load environment variables
# This looks for a .env file and loads the variables defined there.
# It's a secure way to keep secrets like API keys out of your main code.
load_dotenv()

# 2. Configure the Gemini API
# We get the API key from the environment variables we just loaded.
# If you don't have a .env file, you can technically put the string here,
# but it's not recommended for security!
api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key was found
if not api_key:
    print("Warning: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)

# 3. Create the model
# We select the 'gemini-pro' model which is good for text-based chat.
model = genai.GenerativeModel('gemini-flash-latest')

# 4. Initialize the Flask application
# 'app' is our website object.
app = Flask(__name__)

# --- ROUTES ---
# Routes tell the app what to do when a user visits a specific URL.

# Route for the Home Page
@app.route('/')
def index():
    """
    This function runs when someone visits the homepage ('/').
    It simply sends the 'index.html' file to their browser.
    """
    # render_template serves an HTML file from the 'templates' folder.
    return render_template('index.html')

# Route for the Chat Functionality
@app.route('/chat', methods=['POST'])
def chat():
    """
    This function handles the chat messages.
    It receives a message from the user (via JavaScript),
    sends it to Gemini, and returns Gemini's answer.
    """
    try:
        # Get the JSON data sent by the frontend (script.js)
        data = request.get_json()
        user_message = data.get('message')

        # Check if the message is empty
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Send the message to Gemini
        # We assume a fresh chat every time for simplicity in this mini-project.
        response = model.generate_content(user_message)

        # Get the text from Gemini's response
        bot_reply = response.text

        # Send the reply back to the frontend as JSON
        return jsonify({'reply': bot_reply})

    except Exception as e:
        # If something goes wrong (like no internet, or API error),
        # print the error to the terminal and send an error message to the user.
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# 5. Run the Application
# This block ensures the app only runs if we execute this file directly.
if __name__ == '__main__':
    # debug=True allows the app to reload automatically when we change code.
    app.run(debug=True)
