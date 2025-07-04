"""
WSGI config for Havencraft project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from HandmadeMart.app import create_app

# Create the Flask application
app = create_app()

# Initialize database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
