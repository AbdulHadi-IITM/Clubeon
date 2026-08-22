from flask import request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.assistant import assistant_bp
from app.assistant.services import AssistantService
from app.auth.models import User

@assistant_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    if not data or not data.get('message'):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Message is required"}), 400
    
    message = data['message']
    if len(message) > 2000:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Message exceeds 2000 characters"}), 400
    
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    
    if user.role == 'owner':
        return jsonify({"code": "FORBIDDEN", "message": "Owner not allowed in Phase 1"}), 403
        
    thread_messages = session.get('assistant_thread_messages', None)
    user_lat = data.get('user_lat')
    user_lon = data.get('user_lon')
    
    result, status = AssistantService.process_chat(
        user=user,
        message=message,
        thread_messages=thread_messages,
        user_lat=user_lat,
        user_lon=user_lon
    )
    
    if status == 200:
        # Save state in session
        session['assistant_thread_messages'] = result['thread_messages']
        
        return jsonify({
            "assistant_message": result["assistant_message"],
            "response_id": result["response_id"],
            "tools_used": result["tools_used"]
        }), 200
        
    return jsonify(result), status
