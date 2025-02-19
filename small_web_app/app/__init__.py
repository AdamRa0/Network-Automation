from flask import Flask
from routes.interfaces import interface_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(interface_bp)

    return app