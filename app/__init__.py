"""
Sleep Data Visualization Flask application.
"""
import os
from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Register blueprints
    from app.views.main import main_bp
    from app.views.dashboard import dashboard_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)

    # Create a route to test the app
    @app.route('/test')
    def test_page():
        return 'The Sleep Data Visualization app is running!'

    return app