from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuration
    app.config.from_object('app.config.Config')
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main.bp)
    
    return app 