from flask import request, jsonify, send_file, abort, current_app as my_app
from models.post import Post
from models.user import User
from app import db
from . import api
import uuid
from io import BytesIO
from extensions import db

@api.route('/image/<name>', methods=['GET'])
def get_post_image(name):
    post = Post.query.filter_by(
        image_name=name
    ).first()

    if (post is None):
        abort(404)

    return send_file(BytesIO(post.image_data), download_name=post.image_name)