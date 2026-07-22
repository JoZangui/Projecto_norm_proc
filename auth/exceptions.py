# auth/exceptions.py
class DomainNotAuthorized(Exception):
    """Dominio não está ativo em AcceptedDomain."""
    pass
