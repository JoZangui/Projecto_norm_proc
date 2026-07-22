# utils/identifiers.py
"""
funções utilitárias para geração de identificadores únicos.
Usa UUIDv7 para gerar identificadores sequenciais.
nota: UUIDv7 é uma especificação recente e pode não ser suportada em todas as bibliotecas. Por isso, usamos a biblioteca uuid6 que suporta UUIDv6 e UUIDv7.
"""

from uuid6 import uuid6

def generate_sequential_uuid():
    """ Gera um UUIDv6 sequencial."""
    return uuid6()
