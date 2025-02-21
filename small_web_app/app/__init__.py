from flask import Flask
from routes.interfaces import interface_bp
from routes.vlans import vlan_bp

def create_app():
    app = Flask(__name__, template_folder="../templates")
    
    app.register_blueprint(interface_bp)
    app.register_blueprint(vlan_bp)

    return app