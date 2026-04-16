from app import db
from sqlalchemy.exc import SQLAlchemyError

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

    @staticmethod
    def create(name):
        """
        建立新分類。
        :param name: 分類名稱
        :return: Category 物件或 None
        """
        try:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            return category
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating category: {e}")
            return None

    @staticmethod
    def get_all():
        """
        取得所有分類。
        :return: Category 物件列表
        """
        try:
            return Category.query.all()
        except SQLAlchemyError as e:
            print(f"Error getting all categories: {e}")
            return []

    @staticmethod
    def get_by_id(category_id):
        """
        根據 ID 取得分類。
        :param category_id: 分類 ID
        :return: Category 物件或 None
        """
        try:
            return Category.query.get(category_id)
        except SQLAlchemyError as e:
            print(f"Error getting category by id {category_id}: {e}")
            return None

    @staticmethod
    def update(category_id, name):
        """
        更新分類名稱。
        :param category_id: 分類 ID
        :param name: 新名稱
        :return: 更新後的 Category 物件或 None
        """
        try:
            category = Category.get_by_id(category_id)
            if category:
                category.name = name
                db.session.commit()
            return category
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating category {category_id}: {e}")
            return None

    @staticmethod
    def delete(category_id):
        """
        刪除分類。
        :param category_id: 分類 ID
        :return: Boolean 是否成功
        """
        try:
            category = Category.get_by_id(category_id)
            if category:
                db.session.delete(category)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting category {category_id}: {e}")
            return False
