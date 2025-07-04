import sys
import os

# Add the parent directory to the Python path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

# Now import the app
from HandmadeMart.app import app as application

if __name__ == "__main__":
    application.run()
