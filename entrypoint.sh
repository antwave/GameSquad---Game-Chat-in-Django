#!bin/sh

python gamesquad/manage.py migrate --no-input
python gamesquad/manage.py collectstatic --no-input

daphne -p 8000 -b 0.0.0.0 gamesquad.asgi:application