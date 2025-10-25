FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY .env .

COPY TP_Adopciones ./TP_Adopciones

RUN mkdir -p /data

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["sh", "-c", "python TP_Adopciones/manage.py migrate && python TP_Adopciones/manage.py runserver 0.0.0.0:8000"]