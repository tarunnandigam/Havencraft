import os
import sys
import logging
from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_migrate import Migrate

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import extensions
from extensions import db

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "a_default_secret_key_that_should_be_changed")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# In app.py, update the database configuration section
# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///handmademart.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)

# Import models after db initialization
from models import Category, Product, User, Wishlist, Order, OrderItem, init_sample_data

# Import routes after models are defined
from routes import main as main_blueprint
from auth_routes import auth as auth_blueprint

# Register blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')

def init_db():
    """Initialize the database and create tables."""
    try:
        with app.app_context():
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

# At the bottom of app.py, add:
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Initialize the database when running directly
    init_db()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')