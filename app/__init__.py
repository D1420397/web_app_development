import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本配置
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(app.instance_path, 'database.db')}"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化套件
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 註冊路由
    from app.routes import register_blueprints
    register_blueprints(app)

    return app

def init_db():
    """
    初始化資料庫。
    """
    app = create_app()
    with app.app_context():
        # 這裡根據 schema.sql 初始化，或者直接用 db.create_all()
        # 基於 db-design skill，我們有 schema.sql
        db_path = os.path.join(app.instance_path, 'database.db')
        if not os.path.exists(db_path):
            db.create_all()
            print("Database initialized.")
        else:
            print("Database already exists.")
