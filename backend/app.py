#!/usr/bin/env python3
from flask import Flask, jsonify
from extensions import db, bcrypt, jwt
from swagger import swagger_ui_blueprint, SWAGGER_URL, spec
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    
    # Inicjalizacja rozszerzeń
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Rejestracja blueprintów
    from routes import api
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/api/swagger.json')
    def create_swagger_spec():
        return jsonify(spec.to_dict())

    @app.route('/')
    def index():
        return jsonify(message="Hello from Flask!")
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
