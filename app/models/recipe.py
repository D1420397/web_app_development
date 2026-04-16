from datetime import datetime
try:
    from app import db
except ImportError:
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

# 匯入關聯表以供 relationship 使用
from app.models.ingredient import recipe_ingredients

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 關聯
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, backref=db.backref('recipes', lazy='dynamic'))

    def __repr__(self):
        return f'<Recipe {self.title}>'

    @staticmethod
    def create(title, instructions, author_id, description=None, image_path=None, category_id=None, ingredients=None):
        recipe = Recipe(
            title=title, 
            instructions=instructions, 
            author_id=author_id, 
            description=description, 
            image_path=image_path, 
            category_id=category_id
        )
        if ingredients:
            recipe.ingredients = ingredients
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @staticmethod
    def get_all():
        return Recipe.query.all()

    @staticmethod
    def get_by_id(recipe_id):
        return Recipe.query.get(recipe_id)

    @staticmethod
    def update(recipe_id, **kwargs):
        recipe = Recipe.get_by_id(recipe_id)
        if recipe:
            for key, value in kwargs.items():
                if hasattr(recipe, key):
                    setattr(recipe, key, value)
            db.session.commit()
        return recipe

    @staticmethod
    def delete(recipe_id):
        recipe = Recipe.get_by_id(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return True
        return False
