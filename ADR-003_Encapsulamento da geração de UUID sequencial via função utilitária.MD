## ADR-003: Encapsulamento da geração de UUID sequencial via função utilitária

**Status:** Aceito  
**Data:** 2025-09-07  
**Contexto:** A aplicação utiliza `UUIDField` como chave primária em todos os modelos principais, com geração sequencial baseada em UUIDv7. A lógica de geração será centralizada em uma função utilitária para garantir consistência e facilitar evolução.

---

### Decisão

Criar uma função utilitária chamada `generate_sequential_uuid()` no módulo `utils.identifiers`, responsável por gerar UUIDs sequenciais (UUIDv7) para uso como chave primária em modelos da aplicação.

```python
# utils/identifiers.py
from uuid6 import uuid6

def generate_sequential_uuid():
  return uuid7()
```

---

### Aplicação nos modelos

Todos os modelos que usam `UUIDField` como chave primária devem referenciar essa função:

```python
id = models.UUIDField(primary_key=True, default=generate_sequential_uuid, editable=False)
```

---

### Justificativa

#### Centralização da lógica
- Evita duplicação de chamadas a `uuid7()` em múltiplos arquivos.
- Facilita manutenção e evolução futura (ex: troca por ULID, prefixos por subsidiária).

#### Testabilidade
- Permite uso de mocks em testes automatizados:
```python
@patch('utils.identifiers.generate_sequential_uuid')
def test_model_creation(mock_uuid):
    mock_uuid.return_value = UUID('0188d0f2-...')
```

#### Evolução arquitetural
- Pode incorporar lógica adicional no futuro:
  - Logging de geração
  - Prefixo por subsidiária
  - Validação ou formatação customizada

#### Consistência entre apps
- Garante que todos os modelos compartilhem o mesmo padrão de identificador.
- Facilita rastreabilidade entre entidades de diferentes apps (ex: `users`, `documents`, `audit`).

---

### Trade-offs

| Aspecto        | Impacto |
|----------------|---------|
| **Overhead mínimo** | Uma função extra, mas com grande ganho em clareza e manutenção. |
| **Dependência externa** | Requer a biblioteca `uuid6`, que deve ser mantida atualizada. |

---

### Alternativas consideradas

| Alternativa        | Motivo da rejeição |
|--------------------|--------------------|
| Uso direto de `uuid7()` em cada modelo | Duplica lógica, dificulta testes e evolução. |
| Uso de `uuid4()` aleatório | Menor performance em índices, sem ordenação temporal. |
| Uso de `AutoField` | Previsível, inseguro e não escalável entre subsidiárias. |

---

### Impacto arquitetural

- Todos os modelos devem importar e usar `generate_sequential_uuid()` como `default` em `UUIDField`.
- Testes automatizados podem mockar a função para garantir previsibilidade.
- A função pode evoluir para suportar prefixos, logs ou validações sem alterar os modelos.

---

Se quiser, posso montar o próximo ADR sobre versionamento de documentos com rastreabilidade entre revisões e justificativas. Só dizer.
