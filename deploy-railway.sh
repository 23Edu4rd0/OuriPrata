#!/usr/bin/env bash
#
# Provisiona e publica a OuriPrata no Railway.
#
# Pré-requisito: rodar `railway login` antes (abre o navegador para autenticar).
# Depois é só: ./deploy-railway.sh
#
# O script é seguro para rodar de novo: pula o que já existe.

set -euo pipefail

PROJETO="${PROJETO:-ouriprata}"
MONTAGEM="/app/media"

info() { printf '\n\033[1;33m==> %s\033[0m\n' "$1"; }
erro() { printf '\n\033[1;31mERRO: %s\033[0m\n' "$1" >&2; exit 1; }

# --- 1. Autenticação -------------------------------------------------------
info "Verificando autenticação"
if ! railway whoami >/dev/null 2>&1; then
  erro "Não autenticado. Rode 'railway login' e execute este script de novo."
fi
railway whoami

# --- 2. Projeto ------------------------------------------------------------
if railway status >/dev/null 2>&1; then
  info "Projeto já vinculado a esta pasta"
  railway status
else
  info "Criando o projeto '$PROJETO'"
  railway init --name "$PROJETO"
fi

# --- 3. Banco de dados -----------------------------------------------------
# O Postgres do Railway injeta DATABASE_URL automaticamente no serviço web.
info "Provisionando o PostgreSQL"
railway add --database postgres || echo "(Postgres já existe, seguindo)"

# --- 4. Variáveis de ambiente ---------------------------------------------
# A SECRET_KEY é gerada aqui e nunca sai desta máquina a não ser para o
# Railway. Se já existir uma no serviço, ela é mantida.
info "Configurando variáveis"

if railway variables --kv 2>/dev/null | grep -q '^SECRET_KEY='; then
  echo "SECRET_KEY já definida, mantendo a existente"
else
  echo "Gerando SECRET_KEY nova"
  CHAVE="$(python3 -c 'import secrets; print(secrets.token_urlsafe(64))')"
  railway variables --set "SECRET_KEY=$CHAVE" --skip-deploys
  unset CHAVE
fi

# DJANGO_ENV escolhe config/settings/prod.py, que recusa subir com a chave de
# desenvolvimento, sem banco ou sem ALLOWED_HOSTS. Dentro do Railway o padrão
# já seria production; definir explicitamente deixa o ambiente visível no painel.
railway variables \
  --set "DJANGO_ENV=production" \
  --set "MEDIA_ROOT=$MONTAGEM" \
  --skip-deploys

# No primeiro deploy o domínio ainda não foi gerado, então RAILWAY_PUBLIC_DOMAIN
# vem vazia e o prod.py abortaria já na migração por ALLOWED_HOSTS vazia. O
# curinga cobre qualquer domínio que o Railway venha a gerar; assim que houver um
# domínio próprio, troque por ele:
#
#   railway variables --set "ALLOWED_HOSTS=ouriprata.com.br" \
#                     --set "CSRF_TRUSTED_ORIGINS=https://ouriprata.com.br"
#
# Por isso o `if`: quem já ajustou não perde o ajuste ao rodar o script de novo.
if railway variables --kv 2>/dev/null | grep -q '^ALLOWED_HOSTS='; then
  echo "ALLOWED_HOSTS já definida, mantendo a existente"
else
  echo "Definindo ALLOWED_HOSTS provisória (domínios do Railway)"
  railway variables \
    --set "ALLOWED_HOSTS=.up.railway.app" \
    --set "CSRF_TRUSTED_ORIGINS=https://*.up.railway.app" \
    --skip-deploys
fi

# --- 5. Volume persistente -------------------------------------------------
# Sem isto as fotos das peças enviadas pelo admin somem no próximo deploy:
# o disco do container é descartável.
info "Criando o volume para as imagens em $MONTAGEM"
if railway volume list 2>/dev/null | grep -q "$MONTAGEM"; then
  echo "Volume já existe, seguindo"
else
  railway volume add --mount-path "$MONTAGEM"
fi

# --- 6. Deploy -------------------------------------------------------------
info "Publicando (o Procfile roda migrate e collectstatic antes de subir)"
railway up --ci

# --- 7. Domínio ------------------------------------------------------------
info "Gerando o domínio público"
railway domain || echo "(domínio já existe)"

cat <<'FIM'

==========================================================
Deploy concluído.

Falta um passo manual — criar o usuário do admin:

    railway run python manage.py createsuperuser

Depois entre em <seu-dominio>/admin/ para cadastrar as peças.
==========================================================
FIM
