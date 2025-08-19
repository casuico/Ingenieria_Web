# salir si hay error
set -o errexit

# actualizar pip
python -m pip install --upgrade pip

# instalar dependencias
python -m pip install -r requirements.txt

# moverse al proyecto
cd TP_Adopciones

# configurar Django
export DJANGO_SETTINGS_MODULE=adopciones_project.settings
export PYTHONPATH=$PWD

# chequear Django
python -m django --version
python manage.py check

# preparar Django
python manage.py collectstatic --no-input --verbosity 2
python manage.py migrate

# crear superusuario
python manage.py createsuperuser --username admin --email "nicolas_clementz@hotmail.com" --noinput || true
