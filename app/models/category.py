try:
    from app import db
except ImportError:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # 關聯
    recipes = db.relationship('Recipe', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

    @staticmethod
    def create(name):
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def get_by_id(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def update(category_id, name):
        category = Category.get_by_id(category_id)
        if category:
            category.name = name
            db.session.commit()
        return category

    @staticmethod
    def delete(category_id):
        category = Category.get_by_id(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False
