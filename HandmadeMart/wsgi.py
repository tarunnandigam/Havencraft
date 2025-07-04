import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Now import the app
from app import app as application

if __name__ == "__main__":
    application.run()
