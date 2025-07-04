release: python -c "from HandmadeMart.app import create_app; app = create_app(); from HandmadeMart.models import db; db.create_all()"
web: gunicorn --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread --timeout 120 --bind 0.0.0.0:$PORT wsgi:application
