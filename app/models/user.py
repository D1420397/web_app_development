from datetime import datetime
from app import db
from sqlalchemy.exc import SQLAlchemyError

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 關聯 (定義在 Recipe 模型中會更清晰，但這裡保留 backref)
    # recipes = db.relationship('Recipe', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def create(username, email, password_hash, is_admin=False):
        """
        建立新使用者。
        :param username: 使用者名稱
        :param email: 電子郵件
        :param password_hash: 雜湊後的密碼
        :param is_admin: 是否為管理員
        :return: User 物件或 None
        """
        try:
            user = User(username=username, email=email, password_hash=password_hash, is_admin=is_admin)
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有使用者。
        :return: User 物件列表
        """
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        """
        根據 ID 取得使用者。
        :param user_id: 使用者 ID
        :return: User 物件或 None
        """
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Error getting user by id {user_id}: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        """
        根據 Email 取得使用者。
        :param email: 電子郵件
        :return: User 物件或 None
        """
        try:
            return User.query.filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error getting user by email {email}: {e}")
            return None

    @staticmethod
    def update(user_id, **kwargs):
        """
        更新使用者資訊。
        :param user_id: 使用者 ID
        :param kwargs: 要更新的欄位與值
        :return: 更新後的 User 物件或 None
        """
        try:
            user = User.get_by_id(user_id)
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating user {user_id}: {e}")
            return None

    @staticmethod
    def delete(user_id):
        """
        刪除使用者。
        :param user_id: 使用者 ID
        :return: Boolean 是否刪除成功
        """
        try:
            user = User.get_by_id(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting user {user_id}: {e}")
            return False
