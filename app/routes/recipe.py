from flask import Blueprint, render_template, redirect, url_for, request, flash
# from flask_login import current_user, login_required
# from app.models.recipe import Recipe

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    首頁：顯示熱門或最新食譜。
    """
    pass

@recipe_bp.route('/search', methods=['GET', 'POST'])
def search():
    """
    食材搜尋。
    GET: 顯示食材勾選頁面。
    POST: 接收勾選清單，渲染搜尋結果。
    """
    pass

@recipe_bp.route('/recipe/create', methods=['GET', 'POST'])
# @login_required
def create():
    """
    發佈食譜。
    GET: 渲染發佈表單。
    POST: 儲存食譜、食材關聯與上傳圖片。
    """
    pass

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """
    查看食譜詳情。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET'])
# @login_required
def edit(id):
    """
    編輯食譜頁面。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/update', methods=['POST'])
# @login_required
def update(id):
    """
    更新食譜。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
# @login_required
def delete(id):
    """
    刪除食譜。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/favorite', methods=['POST'])
# @login_required
def toggle_favorite(id):
    """
    加入或移除收藏。
    """
    pass
