# auth/utils.py
from users_app.models import AcceptedDomain

def get_trusted_domains():
    """
    Retorna a lista de domínios ativos aceitos para autenticação federada.
    """
    return list(
        AcceptedDomain.objects.filter(is_active=True, is_sso_enabled=True)
        .values_list('domain', flat=True)
    )

def get_subsidiary_by_email(email: str):
    """
    Dado um e-mail, retorna a filial associada ao domínio,
    se este domínio estiver ativo em AcceptedDomain.
    Caso contrário, retorna None.
    """
    # 1) Extrai e normaliza o domínio
    try:
        domain = email.split("@", 1)[1].strip().lower()
    except (IndexError, AttributeError):
        return None

    # 2) Consulta o modelo AcceptedDomain
    try:
        accepted = AcceptedDomain.objects.get(domain=domain, is_active=True)
        return accepted.subsidiary
    except AcceptedDomain.DoesNotExist:
        return None

def get_sso_domains() -> list[str]:
    """
    Retorna a lista de domínios que estão ativos e habilitados para SSO via OIDC.
    """
    return list(
        AcceptedDomain.objects
        .filter(is_active=True, is_sso_enabled=True)
        .values_list("domain", flat=True)
    )


def get_sso_domain_map() -> dict[str, str]:
    """
    Retorna um mapeamento {domínio: nome_da_filial} para domínios com SSO.
    """
    return dict(
        AcceptedDomain.objects
        .filter(is_active=True, is_sso_enabled=True)
        .values_list("domain", "subsidiary__name")
    )

def is_sso_enabled(domain: str) -> bool:
    """ Verifica se um domínio específico está habilitado para SSO """
    return AcceptedDomain.objects.filter(
        domain=domain, is_active=True, is_sso_enabled=True
    ).exists()
