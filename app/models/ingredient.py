from datetime import datetime
try:
    from app import db
except ImportError:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

# 多對多關聯表：食譜與食材
recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True),
    db.Column('quantity', db.String(50))
)

# 多對多關聯表：使用者收藏
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Ingredient {self.name}>'

    @staticmethod
    def create(name):
        ingredient = Ingredient(name=name)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient

    @staticmethod
    def get_all():
        return Ingredient.query.all()

    @staticmethod
    def get_by_id(ingredient_id):
        return Ingredient.query.get(ingredient_id)

    @staticmethod
    def get_by_name(name):
        return Ingredient.query.filter_by(name=name).first()

    @staticmethod
    def update(ingredient_id, name):
        ingredient = Ingredient.get_by_id(ingredient_id)
        if ingredient:
            ingredient.name = name
            db.session.commit()
        return ingredient

    @staticmethod
    def delete(ingredient_id):
        ingredient = Ingredient.get_by_id(ingredient_id)
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return True
        return False
