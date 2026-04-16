from flask import Blueprint, render_template
# from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/favorites')
# @login_required
def favorites():
    """
    顯示當前使用者的收藏清單。
    """
    pass

@user_bp.route('/user/recipes')
# @login_required
def my_recipes():
    """
    顯示當前使用者發佈的食譜列表。
    """
    pass
