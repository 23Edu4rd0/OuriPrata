# O Nixpacks do Railway não executa "release:" como uma etapa de deploy à
# parte com rede, ao contrário do Heroku: ele roda esse comando embutido no
# próprio build da imagem, que é isolado e não enxerga a rede privada onde
# fica o Postgres — migrate falhava com "could not translate host name
# postgres.railway.internal". Por isso migrate entra no comando de start, que
# roda em tempo de execução, já com rede.
web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --access-logfile - --error-logfile -
