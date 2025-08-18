# exit on error
set -o errexit

cd TP_Adopciones

# correr migraciones en el contenedor ya conectado a la DB
python manage.py migrate

# crear superusuario si no existe
python manage.py createsuperuser --username admin --email "nicolas_clementz@hotmail.com" --noinput || true

# arrancar el servidor
gunicorn adopciones_project.wsgi:application
