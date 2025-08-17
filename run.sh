# exit on error
set -o errexit

# run the web app server
cd TP_Adopciones
gunicorn TP_Adopciones.wsgi:application