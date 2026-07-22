# auth/oidc_client.py
""" Módulo para interagir com provedores OIDC.
Fornece funções para construir URLs de autorização, trocar códigos por tokens e obter informações do usuário.
"""

import requests
import secrets
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse

from auth.discovery import get_oidc_config

def build_authorization_redirect(request, domain):
    config = get_oidc_config(domain)
    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16)

    request.session['oidc_state'] = state
    request.session['oidc_nonce'] = nonce
    request.session['oidc_domain'] = domain

    params = {
        'client_id': settings.OIDC_RP_CLIENT_ID,
        'response_type': 'code',
        'scope': settings.OIDC_RP_SCOPES,
        'redirect_uri': request.build_absolute_uri(reverse('oidc_callback')),
        'state': state,
        'nonce': nonce,
    }
    return f"{config['authorization_endpoint']}?{urlencode(params)}"

def exchange_code_for_claims(request, code):
    domain = request.session.get('oidc_domain')
    if not domain:
        raise RuntimeError("Domínio OIDC não encontrado na sessão")

    incoming_state = request.GET.get('state')
    if incoming_state != request.session.get('oidc_state'):
        raise RuntimeError("State inválido no callback OIDC")

    config = get_oidc_config(domain)
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': request.build_absolute_uri(reverse('oidc_callback')),
        'client_id': settings.OIDC_RP_CLIENT_ID,
        'client_secret': settings.OIDC_RP_CLIENT_SECRET,
    }
    resp = requests.post(config['token_endpoint'], data=token_data, timeout=5)
    resp.raise_for_status()
    tokens = resp.json()

    headers = {'Authorization': f"Bearer {tokens['access_token']}"}
    ui = requests.get(config['userinfo_endpoint'], headers=headers, timeout=5)
    ui.raise_for_status()
    return ui.json()

def get_authorization_endpoint(domain: str) -> str:
    return get_oidc_config(domain).get("authorization_endpoint")

def get_token_endpoint(domain: str) -> str:
    return get_oidc_config(domain).get("token_endpoint")

def get_userinfo_endpoint(domain: str) -> str:
    return get_oidc_config(domain).get("userinfo_endpoint")

def get_jwks_uri(domain: str) -> str:
    return get_oidc_config(domain).get("jwks_uri")

def get_oidc_endpoints(domain: str) -> dict:
    config = get_oidc_config(domain)
    return {
        "authorization_endpoint": config.get("authorization_endpoint"),
        "token_endpoint": config.get("token_endpoint"),
        "userinfo_endpoint": config.get("userinfo_endpoint"),
        "jwks_uri": config.get("jwks_uri"),
        "issuer": config.get("issuer"),
    }
