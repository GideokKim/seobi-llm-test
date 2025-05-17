from flask import Blueprint, request, jsonify, Response
from openai import AzureOpenAI
from app.core.config import get_settings
from app.db.models import Conversation, Message, MessageRole
from app.db.base import db
import logging
import json

chat_bp = Blueprint('chat', __name__)
settings = get_settings()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure OpenAI 클라이언트 초기화
try:
    logger.info(f"Initializing Azure OpenAI client with endpoint: {settings.azure_openai_endpoint}")
    logger.info(f"Using API version: {settings.azure_openai_api_version}")
    logger.info(f"Using deployment name: {settings.azure_openai_deployment_name}")
    
    if not settings.azure_openai_api_key or settings.azure_openai_api_key == "dummy-key":
        raise ValueError("Azure OpenAI API key is not properly configured")
    if not settings.azure_openai_endpoint or "dummy-endpoint" in settings.azure_openai_endpoint:
        raise ValueError("Azure OpenAI endpoint is not properly configured")
    if not settings.azure_openai_deployment_name or settings.azure_openai_deployment_name == "dummy-deployment":
        raise ValueError("Azure OpenAI deployment name is not properly configured")
    
    client = AzureOpenAI(
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key
    )
    logger.info("Azure OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}", exc_info=True)
    raise

@chat_bp.route('/chat/<int:conversation_id>/completion', methods=['POST'])
def create_chat_completion(conversation_id):
    try:
        # 대화 조회
        conversation = Conversation.query.get_or_404(conversation_id)
        
        # 요청 데이터 가져오기
        data = request.get_json()
        user_message = data.get('message')
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
            
        # 사용자 메시지 저장
        user_msg = Message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=user_message
        )
        db.session.add(user_msg)
        db.session.commit()  # 사용자 메시지를 먼저 저장
        
        # 대화 기록 가져오기 (최근 10개 메시지만)
        recent_messages = Message.query.filter_by(conversation_id=conversation_id)\
            .order_by(Message.created_at.desc())\
            .limit(10)\
            .all()
        
        # 메시지 순서를 시간순으로 정렬
        messages = [
            {"role": msg.role.value, "content": msg.content}
            for msg in reversed(recent_messages)
        ]
        
        # Azure OpenAI API 호출
        response = client.chat.completions.create(
            model=settings.azure_openai_deployment_name,
            messages=messages,
            max_completion_tokens=800
        )
        
        # 응답 메시지 저장
        assistant_message = response.choices[0].message.content
        assistant_msg = Message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=assistant_message
        )
        db.session.add(assistant_msg)
        db.session.commit()
        
        # JSON 응답 생성
        response_data = {
            'conversation_id': conversation_id,
            'message': assistant_message,
            'role': 'assistant',
            'created_at': assistant_msg.created_at.isoformat()
        }
        
        # JSON 응답을 한글이 깨지지 않도록 설정
        return Response(
            json.dumps(response_data, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        )
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in create_chat_completion: {str(e)}", exc_info=True)
        error_message = f"Connection error: {str(e)}"
        return jsonify({'error': error_message}), 500 