import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import the app
from HandmadeMart.app import app as application

if __name__ == "__main__":
    application.run()
