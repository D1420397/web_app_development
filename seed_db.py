from app import create_app, db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.models.category import Category
from werkzeug.security import generate_password_hash

def seed():
    app = create_app()
    with app.app_context():
        # 1. 建立測試使用者
        if not User.get_by_email('test@example.com'):
            user = User.create(
                username='小廚師',
                email='test@example.com',
                password_hash=generate_password_hash('password123'),
                is_admin=True
            )
            print("建立測試使用者成功。")
        else:
            user = User.get_by_email('test@example.com')

        # 2. 建立分類
        if not Category.get_all():
            cat1 = Category.create('中式料理')
            cat2 = Category.create('西式料理')
            print("建立分類成功。")
        else:
            cat1 = Category.get_all()[0]
            cat2 = Category.get_all()[1] if len(Category.get_all()) > 1 else cat1

        # 3. 建立食材與食譜
        recipes_data = [
            {
                'title': '香煎雞胸肉',
                'description': '外酥內嫩的低脂健康料理',
                'instructions': '1. 雞胸肉切片\n2. 灑上鹽與黑胡椒\n3. 熱鍋下橄欖油煎至兩面金黃',
                'category_id': cat2.id,
                'ingredients': ['雞胸肉', '鹽', '黑胡椒', '橄欖油']
            },
            {
                'title': '經典番茄炒蛋',
                'description': '最簡單也最暖心的家常味道',
                'instructions': '1. 番茄切塊，蛋打散\n2. 炒熟雞蛋後盛起\n3. 炒軟番茄，加入蛋與少許鹽翻炒',
                'category_id': cat1.id,
                'ingredients': ['雞蛋', '番茄', '鹽', '糖']
            },
            {
                'title': '蒜香炒時蔬',
                'description': '快速又健康的配菜',
                'instructions': '1. 大蒜切末\n2. 熱鍋炒香大蒜\n3. 加入青菜與少許鹽快速翻炒',
                'category_id': cat1.id,
                'ingredients': ['大蒜', '青菜', '鹽']
            }
        ]

        for data in recipes_data:
            # 處理食材
            ings = []
            for name in data['ingredients']:
                ing = Ingredient.get_by_name(name)
                if not ing:
                    ing = Ingredient.create(name=name)
                ings.append(ing)
            
            # 建立食譜
            Recipe.create(
                title=data['title'],
                description=data['description'],
                instructions=data['instructions'],
                author_id=user.id,
                category_id=data['category_id'],
                ingredients=ings
            )
            print(f"建立食譜：{data['title']} 成功。")

if __name__ == '__main__':
    seed()
