from datetime import datetime
from app import db
from sqlalchemy.exc import SQLAlchemyError
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
    author = db.relationship('User', backref=db.backref('recipes', lazy=True))
    category = db.relationship('Category', backref=db.backref('recipes', lazy=True))
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, backref=db.backref('recipes', lazy='dynamic'))

    def __repr__(self):
        return f'<Recipe {self.title}>'

    @staticmethod
    def create(title, instructions, author_id, description=None, image_path=None, category_id=None, ingredients=None):
        """
        建立新食譜。
        :param title: 標題
        :param instructions: 步驟
        :param author_id: 作者 ID
        :param description: 簡介
        :param image_path: 圖片路徑
        :param category_id: 分類 ID
        :param ingredients: Ingredient 物件列表
        :return: Recipe 物件或 None
        """
        try:
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
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating recipe: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有食譜。
        :return: Recipe 物件列表
        """
        try:
            return Recipe.query.all()
        except SQLAlchemyError as e:
            print(f"Error getting all recipes: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """
        根據 ID 取得食譜。
        :param recipe_id: 食譜 ID
        :return: Recipe 物件或 None
        """
        try:
            return Recipe.query.get(recipe_id)
        except SQLAlchemyError as e:
            print(f"Error getting recipe by id {recipe_id}: {e}")
            return None

    @staticmethod
    def update(recipe_id, **kwargs):
        """
        更新食譜資訊。
        :param recipe_id: 食譜 ID
        :param kwargs: 要更新的欄位與值
        :return: 更新後的 Recipe 物件或 None
        """
        try:
            recipe = Recipe.get_by_id(recipe_id)
            if recipe:
                for key, value in kwargs.items():
                    if hasattr(recipe, key):
                        if key == 'ingredients': # 特殊處理多對多
                            recipe.ingredients = value
                        else:
                            setattr(recipe, key, value)
                db.session.commit()
            return recipe
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating recipe {recipe_id}: {e}")
            return None

    @staticmethod
    def delete(recipe_id):
        """
        刪除食譜。
        :param recipe_id: 食譜 ID
        :return: Boolean 是否成功
        """
        try:
            recipe = Recipe.get_by_id(recipe_id)
            if recipe:
                db.session.delete(recipe)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting recipe {recipe_id}: {e}")
            return False
