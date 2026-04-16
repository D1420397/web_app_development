from flask import Blueprint, render_template
# from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
# @admin_required
def dashboard():
    """
    管理員後台首頁。
    """
    pass

@admin_bp.route('/admin/categories', methods=['GET', 'POST'])
# @admin_required
def manage_categories():
    """
    分類管理。
    """
    pass
