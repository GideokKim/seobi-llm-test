from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

# SQLAlchemy 초기화
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configuration
    app.config.from_object('app.config.Config')
    
    # 데이터베이스 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 데이터베이스 초기화
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main, chat
    app.register_blueprint(main.bp)
    app.register_blueprint(chat.bp)
    
    # 데이터베이스 테이블 생성
    with app.app_context():
        db.create_all()
    
    return app 