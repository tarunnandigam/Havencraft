import os
import logging
from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_migrate import Migrate
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

with app.app_context():
    # Import models first to ensure tables are defined
    from models import init_sample_data
    
    # Import routes after models are defined
    import auth_routes
    import routes
    
    # Create all tables
    db.create_all()
    
    # Initialize sample data if database is empty
    if not db.session.query(db.exists().select_from(db.metadata.tables['product'])).scalar():
        init_sample_data()

# At the bottom of app.py, add:
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Initialize sample data if needed
        from models import init_sample_data
        if not db.session.query(db.exists().select_from(db.metadata.tables['product'])).scalar():
            try:
                init_sample_data()
            except Exception as e:
                app.logger.error(f"Error initializing sample data: {str(e)}")
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')