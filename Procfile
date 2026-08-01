# O release roda num container próprio, cujo disco é descartado depois. Por
# isso só a migração fica aqui: um collectstatic feito no release não chegaria
# ao container que serve o site, e o whitenoise subiria sem o manifesto.
release: python manage.py migrate --noinput
web: python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --access-logfile - --error-logfile -
