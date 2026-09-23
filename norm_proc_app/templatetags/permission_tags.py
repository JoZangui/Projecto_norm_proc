# helpdesk/templatetags/permission_tags.py
"""
Tags de modelo personalizadas para verificações de permissões de usuários.
Este arquivo define filtros de modelo que podem ser usados em templates Django para verificar se um usuário tem uma permissão específica ou qualquer permissão de uma lista.
"""
from django import template

register = template.Library()

@register.filter(name='has_permission')
def has_permission(user, permission_name):
    """Verifica se *user* tem a permissão indicada.

    O valor passado nos templates pode ser a forma completa
    (``app_label.codename``) ou o nome legível exibido no admin
    (por exemplo, ``"Can close the ticket"``).

    Quando for fornecido um nome pontilhado delegamos para
    ``user.has_perm``. Senão, procuramos um objeto ``Permission`` cujo
    ``name`` coincida e construímos a string canónica a partir do
    ``content_type`` e do ``codename``.
    """

    # if the template passed something like "helpdesk.can_close_the_ticket"
    if "." in permission_name:
        result = user.has_perm(permission_name)
        return result

    # otherwise treat the argument as a verbose name
    from django.contrib.auth.models import Permission
    try:
        perm = Permission.objects.get(name=permission_name)
        full_name = f"{perm.content_type.app_label}.{perm.codename}"
        result = user.has_perm(full_name)
        return result
    except Permission.DoesNotExist:
        # print(f"Permission with name '{permission_name}' not found") # TODO: logar isso em vez de printar
        return False

@register.filter(name='has_any_permission')
def has_any_permission(user, permission_names):
    """Retorna ``True`` se o utilizador tiver **qualquer** uma das permissões fornecidas.

    A string *permission_names* pode conter valores separados por vírgula,
    onde cada valor é um nome pontilhado (`app_label.codename`) ou um nome
    legível. Chamamos ``has_permission`` para cada elemento por sua vez e
    interrompemos a leitura assim que uma correspondência for encontrada.
    """

    permission_list = [name.strip() for name in permission_names.split(',')]
    for perm in permission_list:
        if has_permission(user, perm):
            return True
    return False
