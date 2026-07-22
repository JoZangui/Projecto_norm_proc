## ADR-002: Uso de UUID como chave primária em modelos da aplicação

**Status:** Aceito  
**Data:** 2025-09-07  
**Contexto:** Aplicação web corporativa para gestão de normas e procedimentos, utilizada por múltiplas subsidiárias com autonomia operacional e necessidade de rastreabilidade global.

---

### Decisão

Todos os modelos principais da aplicação utilizarão `UUIDField` como chave primária, substituindo o `AutoField` padrão do Django. A geração será feita via UUID sequencial (preferencialmente UUIDv7) e não mais o UUID aleatório, garantindo unicidade global e ordenação temporal.

---

### Modelos afetados

| Modelo              | Campo primário definido |
|---------------------|--------------------------|
| `BaseDocument`      | `id = UUIDField(primary_key=True, default=uuid7, editable=False)` |
| `Norms`    | Herda de `BaseDocument` |
| `Procedures` | Herda de `BaseDocument` |
| `Department`        | `id = UUIDField(...)` |
| `ActionLog`         | `id = UUIDField(...)` |

---

### Justificativa

#### Segurança
- Evita enumeração de objetos via URLs previsíveis.
- UUIDs são difíceis de adivinhar, mesmo em ambientes públicos.

#### Escalabilidade entre subsidiárias
- Cada unidade pode gerar documentos localmente sem risco de colisão.
- Suporte nativo a replicação, sincronização e importação entre ambientes.

#### Performance com UUID sequencial
- Ordenação temporal melhora eficiência de índices B-tree.
- Reduz fragmentação em bancos como PostgreSQL.

#### Interoperabilidade
- Identificadores globais compatíveis com APIs, logs, auditorias e integrações externas.
- Facilita rastreabilidade entre documentos de diferentes subsidiárias.

---

### Trade-offs

| Aspecto        | Impacto |
|----------------|---------|
| **Espaço em disco** | UUIDs ocupam mais bytes que inteiros (128 bits vs 32 bits). |
| **Legibilidade** | Identificadores como `0188d0f2-7f7c-7cc0-bf3a-8b7c3f1e2b5a` são menos intuitivos que `id=42`. |
| **Debug manual** | Consultas SQL e testes manuais exigem copiar UUIDs completos. |

Mitigação: uso de aliases ou slugs legíveis para visualização pública, e ferramentas de admin com busca por título ou acrônimo.

---

### Alternativas consideradas

| Alternativa        | Motivo da rejeição |
|--------------------|--------------------|
| `AutoField`        | Colide facilmente entre bancos distintos, inseguro em URLs. |
| `BigAutoField`     | Escala melhor, mas ainda previsível e dependente do banco. |
| `SlugField` como PK | Legível, mas não garante unicidade global e exige validação adicional. |
| `UUIDv4` aleatório | Seguro, mas impacta performance em índices e ordenação. |

---

### Impacto arquitetural

- Todas as relações entre modelos (`ForeignKey`, `ManyToMany`) devem usar `UUIDField`.
- APIs e serializers devem tratar UUIDs como identificadores padrão.
- Logs e auditoria devem registrar UUIDs para rastreabilidade entre entidades.
- Geração de UUIDs sequenciais será feita via biblioteca como `uuid6` ou `uuid7`.