# Flask Application Entry Point - Main backend server
from flask import Flask  # Web framework for Python
from flask_cors import CORS  # Cross-Origin Resource Sharing
from routes.routes import apiBp  # Import API routes blueprint

app = Flask(__name__)  # Initialize Flask web application
CORS(app)  # Enable CORS for frontend communication

app.register_blueprint(apiBp)  # Register API routes to Flask app

if __name__ == '__main__':  # Run server if script executed directly
    app.run(debug=True)  # Start Flask development server

