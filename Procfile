release: python -c "from HandmadeMart.app import init_db; init_db()"
web: gunicorn --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread --timeout 120 --bind 0.0.0.0:$PORT wsgi:application
