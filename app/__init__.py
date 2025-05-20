from flask import Flask, json
from flask_cors import CORS
from dotenv import load_dotenv
from app.models.db import db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # JSON 인코딩 설정
    app.json.ensure_ascii = False
    app.json.mimetype = 'application/json; charset=utf-8'
    
    # Configuration
    app.config.from_object('app.config.Config')
    
    # 데이터베이스 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 데이터베이스 초기화
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main, message, session, user
    app.register_blueprint(main.bp)
    app.register_blueprint(message.message_bp, url_prefix='/api/messages')
    app.register_blueprint(session.session_bp, url_prefix='/api/sessions')
    app.register_blueprint(user.user_bp, url_prefix='/api/users')
    
    # 데이터베이스 테이블 생성
    with app.app_context():
        db.create_all()
    
    return app 