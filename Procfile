web: python3 manage.py collectstatic --noinput && uwsgi --static-map /static=/workspace/app/static --ini uwsgi.ini

celery_worker: celery -A config.celery:app worker -l info
celery_beat: celery -A config.celery:app beat -l info -S django

migrations: python3 manage.py migrate

tests: pytest
shell_plus: python3 manage.py shell_plus
dbshell: python3 manage.py dbshell
debug: python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:$PORT
health_check: python3 manage.py health_check

freeze: sleep 3000
