from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    顯示與處理註冊請求。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 驗證輸入
        if not username or not email or not password:
            flash('所有欄位皆為必填。', 'error')
            return render_template('auth/register.html')
        
        if User.get_by_email(email):
            flash('該 Email 已被註冊。', 'error')
            return render_template('auth/register.html')
            
        # 建立使用者
        password_hash = generate_password_hash(password)
        user = User.create(username=username, email=email, password_hash=password_hash)
        
        if user:
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，請重試。', 'error')
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    顯示與處理登入請求。
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.get_by_email(email)
        
        if not user or not check_password_hash(user.password_hash, password):
            flash('Email 或密碼錯誤，請重試。', 'error')
            return render_template('auth/login.html')
            
        login_user(user, remember=remember)
        return redirect(url_for('recipe.index'))
        
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """
    清除 Session 並登出使用者。
    """
    logout_user()
    flash('您已成功登出。', 'info')
    return redirect(url_for('recipe.index'))
