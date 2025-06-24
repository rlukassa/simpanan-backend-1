# API Route Definition Layer
from flask import Blueprint  # Flask blueprint for route organization
from controller.controller import handleAskRequest  # Import request handler

apiBp = Blueprint('api', __name__)  # Create API blueprint

@apiBp.route('/ask', methods=['POST'])  # Define POST endpoint /ask
def askEndpoint():  # Main chatbot endpoint
    return handleAskRequest()  # Delegate to controller


