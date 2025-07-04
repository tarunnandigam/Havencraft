import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from HandmadeMart.app import create_app
    
    # Create the application instance
    application = create_app()
    
    # Initialize the database
    with application.app_context():
        from HandmadeMart.models import db
        db.create_all()
        print("Database tables created successfully")
        
except Exception as e:
    print(f"Error initializing application: {str(e)}")
    raise

if __name__ == "__main__":
    application.run()
