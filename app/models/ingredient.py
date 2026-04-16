from datetime import datetime
from app import db
from sqlalchemy.exc import SQLAlchemyError

# 多對多關聯表：食譜與食材
recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id', ondelete='CASCADE'), primary_key=True),
    db.Column('quantity', db.String(50))
)

# 多對多關聯表：使用者收藏
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True),
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
        """
        建立新食材。
        :param name: 食材名稱
        :return: Ingredient 物件或 None
        """
        try:
            ingredient = Ingredient(name=name)
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating ingredient: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有食材。
        :return: Ingredient 物件列表
        """
        try:
            return Ingredient.query.all()
        except SQLAlchemyError as e:
            print(f"Error getting all ingredients: {e}")
            return []

    @staticmethod
    def get_by_id(ingredient_id):
        """
        根據 ID 取得食材。
        :param ingredient_id: 食材 ID
        :return: Ingredient 物件或 None
        """
        try:
            return Ingredient.query.get(ingredient_id)
        except SQLAlchemyError as e:
            print(f"Error getting ingredient by id {ingredient_id}: {e}")
            return None

    @staticmethod
    def get_by_name(name):
        """
        根據名稱取得食材。
        :param name: 名稱
        :return: Ingredient 物件或 None
        """
        try:
            return Ingredient.query.filter_by(name=name).first()
        except SQLAlchemyError as e:
            print(f"Error getting ingredient by name {name}: {e}")
            return None

    @staticmethod
    def update(ingredient_id, name):
        """
        更新食材名稱。
        :param ingredient_id: 食材 ID
        :param name: 新名稱
        :return: 更新後的 Ingredient 物件或 None
        """
        try:
            ingredient = Ingredient.get_by_id(ingredient_id)
            if ingredient:
                ingredient.name = name
                db.session.commit()
            return ingredient
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating ingredient {ingredient_id}: {e}")
            return None

    @staticmethod
    def delete(ingredient_id):
        """
        刪除食材。
        :param ingredient_id: 食材 ID
        :return: Boolean 是否成功
        """
        try:
            ingredient = Ingredient.get_by_id(ingredient_id)
            if ingredient:
                db.session.delete(ingredient)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting ingredient {ingredient_id}: {e}")
            return False
