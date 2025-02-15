from extensions import db, bcrypt
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # One-to-many: posts authored by user.
    posts = relationship('Post', backref='author', lazy=True)
    # Many-to-many: posts liked by user.
    #liked_posts = relationship('Post', secondary='likes', backref='likers')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
