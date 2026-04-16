from datetime import datetime
# 假設 db 會在 app/__init__.py 或 app/extensions.py 中定義
# 這裡先使用一個佔位的匯入，實際開發時需對齊專案結構
try:
    from app import db
except ImportError:
    # 為了演示與單獨測試，如果還沒建立 db 物件則先定義基礎結構
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 關聯
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    favorites = db.relationship('Recipe', secondary='favorites', backref=db.backref('favorited_by', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def create(username, email, password_hash, is_admin=False):
        user = User(username=username, email=email, password_hash=password_hash, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update(user_id, **kwargs):
        user = User.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        return user

    @staticmethod
    def delete(user_id):
        user = User.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
