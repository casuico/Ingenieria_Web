# exit on error
set -o errexit

# install project dependencies
#uv sync
pip install -r requirements.txt

# make sure django has all the things it needs to run
cd TP_Adopciones

# preparar Django
python manage.py collectstatic --no-input
python manage.py migrate

# crear superusuario si no existe
python manage.py createsuperuser --username admin --email "nicolas_clementz@hotmail.com" --noinput || true