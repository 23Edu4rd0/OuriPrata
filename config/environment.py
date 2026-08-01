"""
Escolhe qual módulo de settings carregar.

Fica fora do pacote config.settings de propósito: a decisão precisa acontecer
antes de o Django importar qualquer configuração.

Regra:
  DJANGO_ENV=dev|production  decide explicitamente;
  sem DJANGO_ENV, o padrão é 'production' quando a variável RAILWAY_ENVIRONMENT
  existe (ou seja, rodando dentro do Railway) e 'dev' fora dele.

O padrão sensível ao Railway evita o pior caso: alguém publica sem definir
DJANGO_ENV e o site sobe com DEBUG ligado.
"""

import os

APELIDOS = {
    'dev': 'dev',
    'development': 'dev',
    'local': 'dev',
    'prod': 'prod',
    'production': 'prod',
    'producao': 'prod',
}


def settings_module():
    """Devolve o caminho do módulo de settings do ambiente atual."""
    padrao = 'production' if os.getenv('RAILWAY_ENVIRONMENT') else 'dev'
    nome = os.getenv('DJANGO_ENV', padrao).strip().lower()

    try:
        return f'config.settings.{APELIDOS[nome]}'
    except KeyError:
        raise SystemExit(
            f"DJANGO_ENV='{nome}' não é um ambiente conhecido. "
            f'Use um destes: {", ".join(sorted(APELIDOS))}.'
        ) from None


def configure():
    """Define DJANGO_SETTINGS_MODULE se ainda não veio do ambiente."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module())
