from flask import Flask
from app.config.config import Config
from app.models.database import db
from flask_login import LoginManager

login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='views/templates',
                static_folder='views/static')
    
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    # Register blueprints
    from app.controllers.main import main_bp
    from app.controllers.admin import admin_bp
    from app.controllers.shop import shop_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(shop_bp, url_prefix='/shop')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Import and create admin user if not exists
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
    
    return app