# salir si hay error
set -o errexit

# instalar dependencias
python -m pip install -r requirements.txt

# moverse al proyecto
cd TP_Adopciones

# preparar Django
python manage.py collectstatic --no-input
python manage.py migrate

# crear superusuario
python manage.py createsuperuser --username admin --email "nicolas_clementz@hotmail.com" --noinput || true
