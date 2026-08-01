# Ambientes

O projeto tem dois ambientes, cada um com seu módulo de configuração:

| | Desenvolvimento | Produção |
|---|---|---|
| Módulo | `config/settings/dev.py` | `config/settings/prod.py` |
| `DJANGO_ENV` | `dev` (padrão fora do Railway) | `production` (padrão dentro do Railway) |
| `DEBUG` | `True` | `False`, sem opção de ligar |
| Banco | SQLite (`db.sqlite3`) | Postgres via `DATABASE_URL` (obrigatório) |
| Estáticos | servidos direto, sem hash | whitenoise + manifesto com hash |
| https | não | redirecionamento, HSTS e cookies `Secure` |
| Auto-reload | `django_browser_reload` ligado | app nem é instalado |
| E-mail | impresso no terminal | backend padrão do Django (SMTP) |

O que é comum aos dois fica em `config/settings/base.py`.

Quem escolhe o módulo é `config/environment.py`, chamado por `manage.py`,
`config/wsgi.py` e `config/asgi.py`. O padrão depende de onde o processo roda:
existindo a variável `RAILWAY_ENVIRONMENT`, o ambiente é produção. Assim um
deploy sem `DJANGO_ENV` definido não sobe com `DEBUG` ligado.

`prod.py` recusa iniciar sem `SECRET_KEY`, `DATABASE_URL` e `ALLOWED_HOSTS`.
É proposital: melhor o deploy falhar do que o site ficar no ar inseguro.

## Desenvolvimento

```bash
cp .env.example .env
poetry install
python manage.py migrate
python manage.py runserver
```

Em outro terminal, para recompilar o CSS enquanto edita os templates:

```bash
python manage.py tailwind start
```

## Conferir o comportamento de produção antes do deploy

```bash
task check
```

Roda `manage.py check --deploy` com o settings de produção. Para subir a
aplicação localmente já sob o gunicorn e o whitenoise:

```bash
railway run task prod
```

O `railway run` injeta as variáveis do serviço (incluindo `DATABASE_URL`), então
esse comando conversa com o banco de produção — use só para leitura. Sem o
Railway, defina `SECRET_KEY`, `DATABASE_URL` e `ALLOWED_HOSTS` na mão.

## Deploy

```bash
railway login
./deploy-railway.sh
```

O script cria o projeto, provisiona o Postgres, gera a `SECRET_KEY`, define
`DJANGO_ENV=production`, cria o volume das imagens em `/app/media` e publica.
Rodar de novo é seguro: ele pula o que já existe.

No primeiro deploy o domínio ainda não foi gerado, então `RAILWAY_PUBLIC_DOMAIN`
chega vazia e o `prod.py` abortaria por `ALLOWED_HOSTS` vazia. Por isso o script
define `ALLOWED_HOSTS=.up.railway.app` de largada — um curinga que cobre qualquer
domínio gerado pelo Railway. Ao apontar um domínio próprio, troque:

```bash
railway variables --set "ALLOWED_HOSTS=ouriprata.com.br" \
                  --set "CSRF_TRUSTED_ORIGINS=https://ouriprata.com.br"
```

O script não sobrescreve `ALLOWED_HOSTS` se ela já existir, então esse ajuste
sobrevive às próximas execuções.

O `Procfile` roda `migrate` na etapa de release e `collectstatic` na subida do
processo web — o container de release tem disco próprio, descartado depois, então
um `collectstatic` feito lá não chegaria a quem serve o site.

Depois do primeiro deploy, crie o usuário do admin:

```bash
railway run python manage.py createsuperuser
```

## Variáveis

Todas estão documentadas em `.env.example`. As que a produção usa e o
desenvolvimento ignora: `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `MEDIA_ROOT`,
`SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`.
