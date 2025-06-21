# entry point 
# Entry point backend (tempat inisialisasi aplikasi dan load route)
from flask import Flask
from flask_cors import CORS
from routes.routes import api_bp

app = Flask(__name__) # inisialisasi flask , web server Python yang bakal menjalankan API
CORS(app)  # aktifin CORS, biar backend bissa diakses dari frontend

# Register blueprint
app.register_blueprint(api_bp)
# Mendaftarkan blueprint (kumpulan route/endpoint) dari routes/routes.py ke aplikasi Flask utama. Ini membuat semua endpoint yang didefinisikan di blueprint (api_bp) aktif di server Flask Anda.

# Jadi, bagian ini adalah setup utama agar server Flask siap menerima request dari frontend dan endpoint-endpoint API bisa diakses.

if __name__ == '__main__':
    app.run(debug=True)

