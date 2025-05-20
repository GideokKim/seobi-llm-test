from flask import Blueprint, request, jsonify
from app.models import Session, Message, db
from app.utils.openai_client import get_openai_client, get_completion
import re
from app.models.user import User
from datetime import datetime

session_bp = Blueprint('session', __name__)

def parse_title_and_description(response):
    """OpenAI 응답에서 타이틀과 설명을 추출합니다."""
    # 예시 응답: "타이틀: ...\n설명: ..."
    title = ""
    description = ""
    title_match = re.search(r"타이틀\s*[:：]\s*(.*)", response)
    desc_match = re.search(r"설명\s*[:：]\s*(.*)", response)
    if title_match:
        title = title_match.group(1).strip()
    if desc_match:
        description = desc_match.group(1).strip()
    return title, description

@session_bp.route('', methods=['POST'])
def create_session():
    """새로운 세션을 생성합니다."""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'content' not in data:  # message를 content로 변경
            return jsonify({
                'status': 'error',
                'error': 'user_id와 content가 필요합니다'  # message를 content로 변경
            }), 400

        user_id = data['user_id']
        content = data['content']  # message를 content로 변경
        
        # 사용자 확인
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'status': 'error',
                'error': '사용자를 찾을 수 없습니다'
            }), 404

        # 첫 메시지를 기반으로 세션 제목과 설명 생성
        messages = [
            {"role": "system", "content": "당신은 대화의 맥락을 이해하고 적절한 제목과 설명을 생성하는 AI 어시스턴트입니다."},
            {"role": "user", "content": f"다음 대화의 제목과 설명을 생성해주세요. 제목은 20자 이내로, 설명은 100자 이내로 작성해주세요. 대화 내용: {content}"}
        ]
        
        try:
            client = get_openai_client()
            response = get_completion(client, messages)
            
            # 응답에서 제목과 설명 추출
            lines = response.strip().split('\n')
            title = lines[0].replace('제목:', '').strip()
            description = lines[1].replace('설명:', '').strip() if len(lines) > 1 else content[:100]
            
        except Exception as e:
            print(f"OpenAI API 호출 중 오류 발생: {str(e)}")
            # API 호출 실패 시 기본값 사용
            title = content[:20]
            description = content[:100]

        # 세션 생성
        session = Session(
            user_id=user_id,
            title=title,
            description=description
        )
        db.session.add(session)
        db.session.flush()  # ID 생성을 위해 flush

        # 첫 메시지 저장
        message = Message(
            session_id=session.id,
            user_id=user_id,
            content=content,  # message를 content로 변경
            role='user'
        )
        db.session.add(message)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'data': {
                'id': str(session.id),
                'title': session.title,
                'description': session.description,
                'user_id': str(session.user_id),
                'start_at': session.start_at.isoformat()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error in create_session: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@session_bp.route('', methods=['GET'])
def get_sessions():
    sessions = Session.query.order_by(Session.start_at.desc()).all()
    return jsonify({
        'status': 'success',
        'sessions': [{
            'id': str(s.id),
            'user_id': str(s.user_id),
            'title': s.title,
            'description': s.description,
            'start_at': s.start_at.isoformat(),
            'finish_at': s.finish_at.isoformat() if s.finish_at else None
        } for s in sessions]
    })

@session_bp.route('/<uuid:session_id>', methods=['GET'])
def get_session(session_id):
    session = Session.query.get_or_404(session_id)
    return jsonify({
        'status': 'success',
        'session': {
            'id': str(session.id),
            'user_id': str(session.user_id),
            'title': session.title,
            'description': session.description,
            'start_at': session.start_at.isoformat(),
            'finish_at': session.finish_at.isoformat() if session.finish_at else None
        }
    })

@session_bp.route('/<uuid:session_id>', methods=['PUT'])
def update_session(session_id):
    session = Session.query.get_or_404(session_id)
    data = request.json
    session.title = data.get('title', session.title)
    session.description = data.get('description', session.description)
    session.finish_at = data.get('finish_at', session.finish_at)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'session': {
            'id': str(session.id),
            'user_id': str(session.user_id),
            'title': session.title,
            'description': session.description,
            'start_at': session.start_at.isoformat(),
            'finish_at': session.finish_at.isoformat() if session.finish_at else None
        }
    })

@session_bp.route('/<uuid:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    db.session.delete(session)
    db.session.commit()
    return jsonify({'status': 'success'}), 204

@session_bp.route('/<uuid:session_id>/finish', methods=['POST'])
def finish_session(session_id):
    session = Session.query.get_or_404(session_id)
    if session.finish_at:
        return jsonify({'status': 'error', 'error': '이미 종료된 세션입니다.'}), 400
    session.finish_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'success', 'finish_at': session.finish_at.isoformat()}) 