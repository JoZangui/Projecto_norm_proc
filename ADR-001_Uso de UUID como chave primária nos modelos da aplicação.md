## ADR-001: Uso de UUID como chave primária nos modelos da aplicação

**Status:** Aceito  
**Data:** 2025-09-07  
**Contexto:** Aplicação web para gestão de normas e procedimentos com foco em versionamento, rastreabilidade, segurança e modularidade.

---

### Decisão

Todos os modelos principais da aplicação utilizarão `UUIDField` como chave primária, substituindo o `AutoField` padrão do Django. Isso inclui:

#### `Norms`
```python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

#### `Procedures`
```python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

#### `BaseDocument` (modelo abstrato)
```python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

#### `Department`
```python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

#### `ActionLog` (auditoria)
```python
id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
```

---

### Justificativa

#### Segurança
- Evita enumeração de objetos via URLs previsíveis (`/document/42/` → `/document/43/`).
- UUIDs são aleatórios e difíceis de adivinhar.

#### Escalabilidade
- Suporte nativo a ambientes distribuídos e replicação entre bancos.
- Evita colisões em merges, importações ou múltiplos ambientes.

#### Interoperabilidade
- Identificadores globais compatíveis com APIs REST, logs, integrações externas.
- Facilita rastreamento entre sistemas.

#### Modularidade e desacoplamento
- Identificador não depende da lógica interna do banco.
- Facilita testes, mocks e inserções manuais.

---

### Trade-offs

| Aspecto        | Impacto |
|----------------|---------|
| **Performance** | UUIDs ocupam mais espaço e podem ser menos eficientes em índices. |
| **Legibilidade** | Identificadores como `3fa85f64-5717-4562-b3fc-2c963f66afa6` são menos legíveis que `id=42`. |

Mitigação: uso de índices otimizados e abstração de URLs via slugs ou aliases se necessário.

---

### Alternativas consideradas

- **AutoField padrão do Django**: mais simples, porém inseguro e não escalável.
- **BigAutoField**: melhora o espaço, mas mantém previsibilidade e dependência do banco.
- **SlugField como chave primária**: legível, mas não garante unicidade global e exige validação adicional.

---

### Impacto arquitetural

- Todas as relações entre modelos (`ForeignKey`, `ManyToMany`) devem usar `UUIDField`.
- Serializers, admin e APIs devem tratar UUIDs como identificadores padrão.
- Logs e auditoria podem usar UUIDs para rastreabilidade entre entidades.
