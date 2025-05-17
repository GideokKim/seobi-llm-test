from flask import Blueprint, request, jsonify, Response
from app.db.models import Conversation, Message, MessageRole
from app.db.base import db
import json

conversations_bp = Blueprint('conversations', __name__)

@conversations_bp.route('/conversations', methods=['GET'])
def get_conversations():
    conversations = Conversation.query.order_by(Conversation.updated_at.desc()).all()
    response_data = [conv.to_dict() for conv in conversations]
    return Response(
        json.dumps(response_data, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )

@conversations_bp.route('/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    return Response(
        json.dumps(conversation.to_dict(), ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )

@conversations_bp.route('/conversations', methods=['POST'])
def create_conversation():
    data = request.get_json()
    conversation = Conversation(title=data.get('title'))
    db.session.add(conversation)
    db.session.commit()
    return Response(
        json.dumps(conversation.to_dict(), ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
        status=201
    )

@conversations_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def add_message(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    data = request.get_json()
    
    message = Message(
        conversation_id=conversation_id,
        role=MessageRole(data['role']),
        content=data['content']
    )
    
    db.session.add(message)
    db.session.commit()
    return Response(
        json.dumps(message.to_dict(), ensure_ascii=False),
        mimetype='application/json; charset=utf-8',
        status=201
    )

@conversations_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    db.session.delete(conversation)
    db.session.commit()
    return '', 204 