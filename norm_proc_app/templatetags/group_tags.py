# norm_proc_app/templatetags/group_tags.py
"""
Tags de modelo personalizadas para verificações de grupos de usuários.
Este arquivo define filtros de modelo que podem ser usados em templates Django para verificar se um usuário pertence a um grupo específico ou a qualquer grupo de uma lista.
"""

from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Verifica se o usuário pertence a um grupo específico.
    
    Args:
        user: O objeto de usuário a ser verificado.
        group_name: O nome do grupo a ser verificado.
    
    Returns:
        bool: True se o usuário pertence ao grupo, False caso contrário.
    """
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_any_group')
def has_any_group(user, group_names):
    """
    Verifica se o usuário pertence a qualquer grupo de uma lista de grupos.
    
    Args:
        user: O objeto de usuário a ser verificado.
        group_names: Uma lista de nomes de grupos a serem verificados.
    
    Returns:
        bool: True se o usuário pertence a qualquer um dos grupos, False caso contrário.
    """
    group_list = [name.strip() for name in group_names.split(',')]
    return user.groups.filter(name__in=group_list).exists()
