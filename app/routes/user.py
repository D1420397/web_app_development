from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.recipe import Recipe

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/favorites')
@login_required
def favorites():
    """
    顯示當前使用者的收藏清單。
    """
    # 假設 User 模型有 favorites 關聯
    favs = current_user.favorites
    return render_template('user/favorites.html', recipes=favs)

@user_bp.route('/user/recipes')
@login_required
def my_recipes():
    """
    顯示當前使用者發佈的食譜列表。
    """
    recipes = current_user.recipes
    return render_template('user/recipes.html', recipes=recipes)
