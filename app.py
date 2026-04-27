import os
from flask import Flask
from app.routes.main_routes import main_bp
from app.models.database import init_db

def create_app():
    # 建立 Flask 實例，為了與我們的資料夾結構匹配，手動指定 templates 與 static 路徑
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 載入設定（如用於 Flash messages 的 SECRET_KEY）
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 註冊所有的 Blueprint 路由
    app.register_blueprint(main_bp)

    # 確保開啟伺服器時會初始化資料庫
    with app.app_context():
        init_db()

    return app

app = create_app()

if __name__ == '__main__':
    # 啟動伺服器，開啟 debug 模式以利開發時查錯
    app.run(debug=True)
