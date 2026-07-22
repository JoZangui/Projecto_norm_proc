## ADR-004: Adoção de UUIDv6 como chave primária em substituição ao UUIDv7

**Status:** Aceito  
**Data:** 2025-09-07  
**Contexto:** A aplicação corporativa de normas e procedimentos utiliza `UUIDField` como chave primária em todos os modelos principais. Inicialmente foi considerada a adoção de UUIDv7 por suas propriedades de ordenação temporal e segurança, mas limitações de suporte em bibliotecas e ambientes motivaram a reconsideração.

---

### Decisão

Substituir o uso de `uuid7()` por `uuid6()` como gerador padrão de identificadores únicos nos modelos da aplicação. A função será encapsulada em `utils.identifiers.generate_sequential_uuid()` para garantir consistência e facilitar evolução futura.

```python
# utils/identifiers.py
from uuid6 import uuid6

def generate_sequential_uuid():
    return uuid6()
```

---

### Justificativa

#### Compatibilidade
- `uuid6()` é amplamente suportado por bibliotecas como `uuid6` no Python.
- Evita dependência de especificações ainda em fase de adoção (UUIDv7).

#### Ordenação temporal
- Preserva a ordenação cronológica dos identificadores, melhorando performance em índices B-tree.
- Ideal para rastreabilidade entre documentos e ações em sistemas distribuídos.

#### Segurança
- Evita previsibilidade de identificadores como em `AutoField`.
- Mais seguro que UUIDv1, pois reorganiza os bits para não expor diretamente o MAC address.

#### Modularidade e evolução
- A função encapsulada permite futura troca por UUIDv7, ULID ou outro padrão sem alterar os modelos.
- Facilita testes automatizados com mocks e rastreamento de geração.

---

### Trade-offs

| Aspecto        | Impacto |
|----------------|---------|
| **Exposição parcial de timestamp** | Pode revelar ordem de criação, o que é desejável para rastreabilidade, mas exige cuidado em ambientes públicos. |
| **Dependência de biblioteca externa** | Requer instalação e manutenção da lib `uuid6`. |
| **Não é padrão nativo do Python** | Precisa de importação explícita, mas é estável e bem mantido. |

---

### Alternativas consideradas

| Alternativa        | Motivo da rejeição |
|--------------------|--------------------|
| `UUIDv7`           | Ainda não amplamente suportado em bibliotecas e bancos. |
| `UUIDv4` aleatório | Seguro, mas não ordenável — impacta performance em índices. |
| `AutoField`        | Previsível, inseguro e não escalável entre subsidiárias. |
| `ULID`             | Alternativa válida, mas exigiria mudança de tipo e validação adicional. |

---

### Impacto arquitetural

- Todos os modelos que usam `UUIDField` como chave primária devem referenciar `generate_sequential_uuid()` como `default`.
- APIs, serializers e logs devem tratar UUIDv6 como identificador padrão.
- Testes automatizados podem mockar a função para garantir previsibilidade.
- A função pode evoluir para incorporar prefixos por subsidiária, logging ou validações.

---

Se quiser, posso montar o próximo ADR sobre versionamento de documentos com rastreabilidade entre revisões e justificativas. Só dizer.
