#!/usr/bin/env python3
from flask import Flask, jsonify, send_from_directory
from extensions import db, bcrypt, jwt
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import yaml


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # note: CORS is allowed by default for all hostnames
    # which isn't secure
    CORS(app)

    # Konfiguracja Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Social Media API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Endpoint do serwowania specyfikacji Swagger
    @app.route('/api/swagger.json')
    def swagger():
        try:
            with open('./swagger.yml', 'r', encoding='utf-8') as f:
                return jsonify(yaml.safe_load(f))
        except FileNotFoundError:
            return jsonify({"error": "Swagger file not found"}), 404

    from routes import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify(message="Hello from Flask!")
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
