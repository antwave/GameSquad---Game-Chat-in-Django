#!bin/sh

cd gamesquad

python manage.py migrate --no-input
python manage.py collectstatic --no-input

daphne -p 8000 -b 0.0.0.0 gamesquad.asgi:application