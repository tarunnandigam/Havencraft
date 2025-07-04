"""
WSGI config for Havencraft project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from HandmadeMart.app import create_app

# Create the Flask application
application = create_app()

# Initialize database tables if they don't exist
with application.app_context():
    from HandmadeMart.models import db
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)
