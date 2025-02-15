from flask import request, jsonify, send_file, abort, current_app as my_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post import Post
from models.user import User
from app import db
from . import api
import uuid
from io import BytesIO
from extensions import db

# import logging

# logger = logging.getLogger('werkzeug')

@api.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    results = db.session.query(
        Post, User
    ).join(
        User
    ).all()

    output = []
    for post, user in results:
        output.append({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'date_created': post.date_created.isoformat(),
            'filename': post.image_name,
            'author': user.username
        })
    return jsonify(output)

@api.route('/posts', methods=['POST'])
@jwt_required()
def add_post():
    title = request.form.get('title')
    description = request.form.get('description')
    image_data = request.files['image']

    author_name = get_jwt_identity()

    author = User.query.filter_by(username=author_name).first()
    if (author is None):
        abort(403)

    author_id = author.id

    file_uuid = str(uuid.uuid4())
    post = Post(
        title=title,
        description=description,
        image_data=image_data.read(),
        image_name=file_uuid + "-" + image_data.filename,
        author_id=author_id
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post added'}), 201


@api.route('/posts/<user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    results = db.session.query(
        Post, User
    ).join(
        User
    ).filter(
        Post.author_id == user_id
    ).all()

    output = []
    for post, user in results:
        output.append({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'date_created': post.date_created.isoformat(),
            'filename': post.image_name,
            'author': user.username
        })
    return jsonify(output)