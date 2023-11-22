# Usamos una imagen con Python 3.10.12
FROM python:3.10.12

# Establecemos un directorio para nuestro código
ENV APP /usr/src/app
RUN mkdir $APP
WORKDIR $APP

# Instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# Corremos las migraciones
RUN python manage.py migrate

# Exponemos el puerto donde corre Gunicorn
EXPOSE 8000

# Corremos Gunicorn
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]