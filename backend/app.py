#!/usr/bin/env python3
from flask import Flask, jsonify
from extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

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
