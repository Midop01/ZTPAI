from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.likes import Like
from models.user import User
from app import db
from . import api

@api.route('/post/<post_id>/likes')
def get_likes(post_id):
    likes = Like.query.filter_by(post_id=post_id).all()

    return jsonify({"count": len(likes)})

@api.route('/post/<post_id>/like', methods=['GET'])
@jwt_required()
def is_liked(post_id):
    username = get_jwt_identity()

    user = User.query.filter_by(username=username).first()
    if (user is None):
        abort(403)

    
    like = Like.query.filter_by(
        post_id=post_id,
        user_id=user.id
    ).first()

    return jsonify({'is_liked': not like is None}), 201


@api.route('/post/<post_id>/like', methods=['POST'])
@jwt_required()
def add_like(post_id):
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if (user is None):
        abort(403)

    
    like = Like(
        user_id=user.id,
        post_id=post_id
    )

    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Like added'}), 201
