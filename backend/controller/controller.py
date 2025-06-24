# Request Controller Layer 
from flask import request, jsonify  # Flask HTTP utilities
from services.services import detectIntentService  # Import business logic

def handleAskRequest():  # Handle POST requests to /ask endpoint
    requestData = request.get_json()  # Parse JSON from request body
    userQuestion = requestData.get('question', '') if requestData else ''  # Extract question field
    print(f"DEBUG: Controller received: '{userQuestion}'")  # Log incoming request
    serviceResult = detectIntentService(userQuestion)  # Process through ML pipeline
    print(f"DEBUG: Service returned: {serviceResult}")  # Log service response
    return jsonify(serviceResult)  # Return JSON response
