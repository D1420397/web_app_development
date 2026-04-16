from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.category import Category
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('此頁面僅限管理員存取。', 'error')
            return redirect(url_for('recipe.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/dashboard')
@admin_required
def dashboard():
    """
    管理員後台首頁。
    """
    # 這裡可以獲取一些統計數據
    categories = Category.get_all()
    return render_template('admin/dashboard.html', categories=categories)

@admin_bp.route('/admin/categories', methods=['POST'])
@admin_required
def add_category():
    """
    新增分類。
    """
    name = request.form.get('name')
    if name:
        if Category.create(name):
            flash(f'分類 {name} 已建立。', 'success')
        else:
            flash('建立失敗。', 'error')
    return redirect(url_for('admin.dashboard'))
