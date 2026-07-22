# auth/discovery.py
"""
Módulo para descoberta dinâmica de configuração OpenID Connect (OIDC)
Permite obter endpoints e outras configurações do provedor OIDC baseado no domínio da filial.
Utiliza o padrão de descoberta OIDC (/.well-known/openid-configuration).
"""
import requests
from datetime import datetime, timedelta, timezone

from django.conf import settings

from users_app.models import AcceptedDomain
from .utils import get_trusted_domains
from auth.exceptions import DomainNotAuthorized

# Cache em memória (pode ser adaptado para Redis, DB, etc.)
OIDC_DISCOVERY_CACHE = {}

# Tempo de validade do cache (ex: 24h)
CACHE_TTL = timedelta(hours=settings.OIDC_DISCOVERY_CACHE_TTL_HOURS)

def get_oidc_config(domain):
    """ Obtém a configuração OIDC para um domínio específico via descoberta dinâmica.
    Utiliza cache para evitar múltiplas requisições desnecessárias.
    Levanta DomainNotAuthorized se o domínio não estiver na lista de confiáveis.
    ---
    Args:
        domain (str): Domínio da filial para o qual obter a configuração OIDC.
    Returns:
        dict: Configuração OIDC obtida do endpoint de descoberta.
    Raises:
        DomainNotAuthorized: Se o domínio não estiver autorizado.
        RuntimeError: Se houver falha na obtenção da configuração.
    """
    if domain not in get_trusted_domains():
        raise DomainNotAuthorized(f"Domínio {domain} não está autorizado")

    now = datetime.now(timezone.utc)

    # Verifica se já existe cache válido
    if domain in OIDC_DISCOVERY_CACHE:
        cached = OIDC_DISCOVERY_CACHE[domain]
        if now - cached['timestamp'] < CACHE_TTL:
            return cached['config']

    # Monta URL de descoberta
    accepted = AcceptedDomain.objects.get(domain=domain, is_active=True)
    host = accepted.discovery_host or f"idp.{domain}"
    discovery_url = f"https://{host}/.well-known/openid-configuration"

    try:
        response = requests.get(discovery_url, timeout=5)
        response.raise_for_status()
        config = response.json()

        # Armazena no cache
        OIDC_DISCOVERY_CACHE[domain] = {
            'timestamp': now,
            'config': config
        }

        return config

    except Exception as e:
        raise RuntimeError(f"Falha ao obter configuração OIDC para {domain}: {e}")
