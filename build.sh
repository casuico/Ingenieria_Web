# exit on error
set -o errexit

# install project dependencies
pip install -r requirements.txt

# preparar Django
cd TP_Adopciones
python manage.py collectstatic --no-input
