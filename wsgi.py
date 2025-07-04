"""
WSGI config for Havencraft project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
from HandmadeMart.app import create_app, init_db

# Create the Flask application
application = create_app()

# Initialize the database
init_db()

if __name__ == "__main__":
    application.run()
