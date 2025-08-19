# exit on error
set -o errexit

# install project dependencies
#uv sync
pip install -r requirements.txt

# make sure django has all the things it needs to run
cd TP_Adopciones

echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-not set}"
echo "Python version:"
python --version
pip list

export DJANGO_SETTINGS_MODULE=adopciones_project.settings
export PYTHONPATH=$PWD
echo "DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE"
echo "PYTHONPATH=$PYTHONPATH"

# chequear que Django carga correctamente
python manage.py check

# preparar Django
python manage.py collectstatic --no-input --verbosity 2
python manage.py migrate

# crear superusuario si no existe
python manage.py createsuperuser --username admin --email "nicolas_clementz@hotmail.com" --noinput || true