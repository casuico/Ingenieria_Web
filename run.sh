# exit on error
set -o errexit

# run the web app server
cd TP-Adopciones
gunicorn TP-Adopciones.wsgi:application