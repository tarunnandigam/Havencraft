from .app import create_app, db

# This makes the package importable and allows 'from HandmadeMart import create_app, db'
__all__ = ['create_app', 'db']
