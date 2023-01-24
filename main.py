from flask import Flask, request, jsonify, before_render_template
import os
from controller.Sales.UserController import UserController

app = Flask(__name__)
api_v1_cors_config = {
  "origins": "*",
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Authorization", "Content-Type"]
}

@app.route('/home', methods=['GET'])
def home( domain="" ):
    return "Bienvenido " + os.getenv('DBHOST') , 200


@app.route('/api/user', methods=['GET'])
def get_api_user( domain="" ):
    response = UserController().getUserById()
    return jsonify(response)
