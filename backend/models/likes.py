from extensions import db

class Like(db.Model):
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
