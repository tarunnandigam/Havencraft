import os
import sys
import logging
from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Create the app outside of create_app to avoid circular imports
app = Flask(__name__)

def create_app():
    # Configure logging for debugging
    logging.basicConfig(level=logging.DEBUG)

    # Configure the app
    app.secret_key = os.environ.get("SESSION_SECRET", "a_default_secret_key_that_should_be_changed")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Database configuration - use DATABASE_URL from environment variables
    database_uri = os.environ.get('DATABASE_URL', 'sqlite:///handmademart.db')
    if database_uri.startswith('postgres://'):
        database_uri = database_uri.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'connect_args': {'sslmode': 'require'}
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models after db initialization to avoid circular imports
    from . import models
    
    # Import and register blueprints
    from .routes import main as main_blueprint
    from .auth_routes import auth as auth_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy'}), 200

    return app

def init_db():
    """Initialize the database and create tables."""
    app = create_app()
    with app.app_context():
        from .models import db, Category, init_sample_data
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully")
            
            # Initialize sample data if database is empty
            if not Category.query.first():
                print("Initializing sample data...")
                init_sample_data()
                print("Sample data initialized")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise

if __name__ == '__main__':
    # Initialize the database when running directly
    init_db()
    
    # Create and run the app
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')