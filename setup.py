from setuptools import setup, find_packages

setup(
    name="HavenCraft",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-Login',
        'Werkzeug',
        'psycopg2-binary',
        'python-dotenv',
        'gunicorn'
    ],
)
