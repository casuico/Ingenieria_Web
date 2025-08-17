# exit on error
set -o errexit

# run the web app server
cd TP-Adopciones
uv run gunicorn $(dirname $(find . | grep wsgi.py$) | sed "s/\.\///g").wsgi:application