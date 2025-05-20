from flask import Blueprint, request, jsonify
from app.utils.openai_client import get_openai_client, get_completion

bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@bp.route('/completion', methods=['POST'])
def chat_completion():
    """채팅 완성 API 엔드포인트"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': '메시지가 필요합니다'}), 400

        # 시스템 메시지와 사용자 메시지 구성
        messages = [
            {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다. 응답은 간결하고 명확하게 해주세요."},
            {"role": "user", "content": data['message']}
        ]

        # 이전 대화 기록이 있다면 추가
        if 'history' in data:
            messages[1:1] = data['history']

        # OpenAI 클라이언트 초기화 및 응답 생성
        client = get_openai_client()
        response = get_completion(client, messages)

        return jsonify({
            'status': 'success',
            'message': data['message'],  # 사용자 메시지도 함께 반환
            'response': response.strip()  # 불필요한 공백 제거
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 