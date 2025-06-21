# route nya  Definisi endpoint API
# Endpoint: /ask, /intents, dll

from flask import Blueprint #import Blueprint untuk membuat blueprint Flask
from controller.controller import handle_ask #import fungsi handle_ask dari controller untuk menangani logika permintaan API

api_bp = Blueprint('api', __name__) # buat blueprint yaitu api, yang bakal nampung semua route API

# route buat ask chatbot
@api_bp.route('/ask', methods=['POST']) # mendefinisikan route /ask dengan metode POST
def ask():
    return handle_ask()


