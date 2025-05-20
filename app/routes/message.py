from flask import Blueprint, request, jsonify
from app.models import Message, Session, db
from app.utils.openai_client import get_openai_client, get_completion

message_bp = Blueprint('message', __name__)

@message_bp.route('', methods=['POST'])
def create_message():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({'status': 'error', 'error': '메시지 내용이 필요합니다'}), 400
        
    session_id = data.get('session_id')
    user_id = data.get('user_id')
    content = data.get('content')
    role = data.get('role', 'user')
    
    message = Message(session_id=session_id, user_id=user_id, content=content, role=role)
    db.session.add(message)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': {
            'id': str(message.id),
            'session_id': str(message.session_id),
            'user_id': str(message.user_id),
            'content': message.content,
            'role': message.role,
            'timestamp': message.timestamp.isoformat(),
            'vector': list(message.vector) if message.vector else None
        }
    }), 201

@message_bp.route('', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return jsonify({
        'status': 'success',
        'messages': [{
            'id': str(m.id),
            'session_id': str(m.session_id),
            'user_id': str(m.user_id),
            'content': m.content,
            'role': m.role,
            'timestamp': m.timestamp.isoformat(),
            'vector': list(m.vector) if m.vector else None
        } for m in messages]
    })

@message_bp.route('/<uuid:message_id>', methods=['GET'])
def get_message(message_id):
    message = Message.query.get_or_404(message_id)
    return jsonify({
        'status': 'success',
        'message': {
            'id': str(message.id),
            'session_id': str(message.session_id),
            'user_id': str(message.user_id),
            'content': message.content,
            'role': message.role,
            'timestamp': message.timestamp.isoformat(),
            'vector': list(message.vector) if message.vector else None
        }
    })

@message_bp.route('/<uuid:message_id>', methods=['PUT'])
def update_message(message_id):
    message = Message.query.get_or_404(message_id)
    data = request.json
    message.content = data.get('content', message.content)
    message.role = data.get('role', message.role)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': {
            'id': str(message.id),
            'session_id': str(message.session_id),
            'user_id': str(message.user_id),
            'content': message.content,
            'role': message.role,
            'timestamp': message.timestamp.isoformat(),
            'vector': list(message.vector) if message.vector else None
        }
    })

@message_bp.route('/<uuid:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'status': 'success'}), 204

@message_bp.route('/session/<uuid:session_id>/completion', methods=['POST'])
def create_completion(session_id):
    """채팅 완성 API 엔드포인트"""
    try:
        session = Session.query.get_or_404(session_id)
        data = request.json
        if not data or 'content' not in data:
            return jsonify({'status': 'error', 'error': '메시지가 필요합니다'}), 400

        # 사용자 메시지 저장
        user_message = Message(
            session_id=session_id,
            user_id=data.get('user_id'),
            role='user',
            content=data['content']
        )
        db.session.add(user_message)

        # 이전 대화 기록 가져오기
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in session.messages
        ]

        # 시스템 메시지와 사용자 메시지 구성
        messages = [
            {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다. 응답은 간결하고 명확하게 해주세요."},
            *history,
            {"role": "user", "content": data['content']}
        ]

        # OpenAI 클라이언트 초기화 및 응답 생성
        client = get_openai_client()
        response = get_completion(client, messages)

        # AI 응답 저장
        assistant_message = Message(
            session_id=session_id,
            user_id=data.get('user_id'),
            role='assistant',
            content=response
        )
        db.session.add(assistant_message)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'messages': {
                'user_message': {
                    'id': str(user_message.id),
                    'content': user_message.content,
                    'role': user_message.role,
                    'timestamp': user_message.timestamp.isoformat()
                },
                'assistant_message': {
                    'id': str(assistant_message.id),
                    'content': assistant_message.content,
                    'role': assistant_message.role,
                    'timestamp': assistant_message.timestamp.isoformat()
                }
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500 