from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.comment import Comment
from app import db
from . import api

@api.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    content = data.get('content')
    post_id = data.get('post_id')
    user_id = get_jwt_identity()

    comment = Comment(content=content, post_id=post_id, user_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added'}), 201

@api.route('/comments/<int:post_id>', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()

    output = []
    for comment in comments:
        output.append({
            'id': comment.id,
            'content': comment.content,
            'date_created': comment.date_created.isoformat()
        })
    return jsonify(output)
