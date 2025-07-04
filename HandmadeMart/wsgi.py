import sys
import os

# Add the parent directory to the Python path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

# Now import the app
from app import app, init_db

# Initialize the database
init_db()

application = app

if __name__ == "__main__":
    application.run()
