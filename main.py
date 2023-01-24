from flask import Flask, request, jsonify, before_render_template
app = Flask(__name__)
api_v1_cors_config = {
  "origins": "*",
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Authorization", "Content-Type"]
}

@app.route('/home', methods=['GET'])
def home( domain="" ):
    return "Bienvenido", 200
