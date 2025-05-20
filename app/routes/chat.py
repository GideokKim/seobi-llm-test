from flask import Blueprint, request, jsonify
from app.utils.openai_client import get_openai_client, get_completion
from app.models.chat import Conversation, Message
from app import db

bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@bp.route('/conversations', methods=['GET'])
def get_conversations():
    """대화 목록을 조회합니다."""
    conversations = Conversation.query.order_by(Conversation.updated_at.desc()).all()
    return jsonify({
        'status': 'success',
        'conversations': [conv.to_dict() for conv in conversations]
    })

@bp.route('/conversations', methods=['POST'])
def create_conversation():
    """새 대화를 생성합니다."""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': '제목이 필요합니다'}), 400

    conversation = Conversation(title=data['title'])
    db.session.add(conversation)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'conversation': conversation.to_dict()
    }), 201

@bp.route('/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """특정 대화를 조회합니다."""
    conversation = Conversation.query.get_or_404(conversation_id)
    return jsonify({
        'status': 'success',
        'conversation': conversation.to_dict()
    })

@bp.route('/conversations/<int:conversation_id>/completion', methods=['POST'])
def chat_completion(conversation_id):
    """채팅 완성 API 엔드포인트"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': '메시지가 필요합니다'}), 400

        # 사용자 메시지 저장
        user_message = Message(
            conversation_id=conversation_id,
            role='user',
            content=data['message']
        )
        db.session.add(user_message)

        # 이전 대화 기록 가져오기
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]

        # 시스템 메시지와 사용자 메시지 구성
        messages = [
            {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다. 응답은 간결하고 명확하게 해주세요."},
            *history,
            {"role": "user", "content": data['message']}
        ]

        # OpenAI 클라이언트 초기화 및 응답 생성
        client = get_openai_client()
        response = get_completion(client, messages)

        # AI 응답 저장
        assistant_message = Message(
            conversation_id=conversation_id,
            role='assistant',
            content=response
        )
        db.session.add(assistant_message)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': data['message'],
            'response': response.strip(),
            'conversation_id': conversation_id
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 