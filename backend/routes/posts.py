from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post import Post
from app import db
from . import api

@api.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    # Minimal serialization for demonstration.
    output = []
    for post in posts:
        output.append({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'date_created': post.date_created.isoformat()
        })
    return jsonify(output)

@api.route('/posts', methods=['POST'])
@jwt_required()
def add_post():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    image_url = data.get('image_url')
    author_id = get_jwt_identity()
    # Data validation omitted for brevity.
    post = Post(title=title, description=description, image_url=image_url, author_id=author_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post added'}), 201
