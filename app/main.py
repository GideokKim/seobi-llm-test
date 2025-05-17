from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from app.core.config import get_settings
from app.db.base import db
from app.api.conversations import conversations_bp
from app.api.chat import chat_bp

settings = get_settings()

def create_app():
    app = Flask(__name__)
    
    # 설정 로드
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = settings.secret_key
    
    # CORS 설정
    CORS(app, resources={r"/*": {"origins": settings.cors_origins}})
    
    # 데이터베이스 초기화
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Blueprint 등록
    app.register_blueprint(conversations_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    @app.route('/')
    def root():
        return jsonify({"message": "Welcome to Seobi LLM Test API"})
    
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"})
    
    @app.route('/env-check')
    def env_check():
        from app.core.config import get_settings
        settings = get_settings()
        return {
            "azure_openai_api_key": settings.azure_openai_api_key,
            "azure_openai_endpoint": settings.azure_openai_endpoint,
            "azure_openai_api_version": settings.azure_openai_api_version,
            "azure_openai_deployment_name": settings.azure_openai_deployment_name,
            "database_url": settings.database_url,
            "secret_key": settings.secret_key,
            "environment": settings.environment,
            "cors_origins": settings.cors_origins,
        }
    
    return app 