# controller 
# Handle logic request API (seperti pengambilan intent, jawaban, dll)

from flask import request, jsonify 
# Mengimpor objek request (untuk mengambil data dari request user) dan jsonify (untuk mengembalikan response dalam format JSON).

from services.services import detectIntentService #import services

def handle_ask():
    data = request.get_json() #ambil json 
    question = data.get('question', '') # ambil "question" dari json, defaultnya kosong  
    result = detectIntentService(question) # deteksi intent dengan service
    return jsonify(result) # kembalikan hasil dalam format JSON
