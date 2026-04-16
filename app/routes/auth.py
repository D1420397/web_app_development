from flask import Blueprint, render_template, redirect, url_for, request, flash
# from flask_login import login_user, logout_user, login_required
# from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    顯示與處理註冊請求。
    GET: 渲染註冊頁面。
    POST: 建立使用者，成功後重導向至登入或首頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示與處理登入請求。
    GET: 渲染登入頁面。
    POST: 驗證使用者並建立 Session。
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    清除 Session 並登出使用者。
    重導向至首頁。
    """
    pass
