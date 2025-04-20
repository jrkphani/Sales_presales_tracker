"""
Application Factory Module
Creates and configures the Flask application
"""

from flask import Flask
from app.config.settings import load_config
from app.api.routes import register_routes
from app.api.error_handlers import register_error_handlers

def create_app():
    """
    Application factory function that creates and configures
    a new Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    load_config(app)
    
    # Register routes and error handlers
    register_routes(app)
    register_error_handlers(app)
    
    return app 