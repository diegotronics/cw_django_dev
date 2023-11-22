release: python manage.py migrate
web: gunicorn quizes.wsgi:application --preload --workers 2 --timeout 120
