# ADR-005: Uso de UUID em URLs e chave primária

- Status: Accepted
- Date: 2026-09-01

## Contexto

A aplicação usa UUID como chave primária para os modelos de documentos, incluindo `Norms` e `Procedures`, através de uma função utilitária que gera UUIDs sequenciais. Essa decisão foi tomada para evitar IDs previsíveis e para manter a identidade dos registos mais robusta em contextos de negócio e segurança.

Durante a implementação das views e rotas para detalhes de norma e procedimento, verificou-se que a URL também tinha de refletir esse identificador. O código inicial usava `int` nas rotas e os redirects falhavam ao tentar resolver UUIDs.

## Decisão

Vamos manter UUID como identificador primário e também usar UUID nas URLs de detalhe e nos redirects relacionados.

A rota de detalhe deve aceitar UUIDs, e o redirect após criação de um registo deve usar o `pk` do objeto guardado, em vez de tentar usar uma propriedade inexistente do formulário.

Exemplo:

- Modelo: `UUIDField(primary_key=True)`
- Rota: `path('norm_details/<uuid:norm_id>/', ...)`
- Redirect: `reverse('norm_proc_app:norm_details', kwargs={'norm_id': new_norm.pk})`

## Justificação

1. Consistência com a modelagem atual do sistema.
2. Evita IDs sequenciais previsíveis e facilmente enumeráveis.
3. Mantém o design uniforme entre base de dados, modelos e URLs.
4. Reduz riscos de acesso/enumeração indevida em objetos sensíveis.

## Consequências

### Positivas

- URLs e chaves primárias mantêm um padrão coerente.
- Os redirects e as rotas ficam alinhados com o modelo de dados.
- O sistema fica preparado para identificadores globais e menos previsíveis.

### Negativas

- As URLs ficam menos curtas e menos amigáveis para leitura manual.
- Em cenários totalmente internos, `int` poderia ser mais simples de usar.
- Testes manuais e navegação direta podem parecer menos intuitivos.

## Alternativas consideradas

### 1. Usar `id` inteiro como chave primária

- Vantagem: URLs mais simples e curtas.
- Desvantagem: inconsistente com a estratégia atual da aplicação e menos robusto para exposição pública.

### 2. Usar UUID apenas para a base de dados e `int` nas URLs

- Vantagem: URLs mais legíveis.
- Desvantagem: mistura de tipos entre a realidade persistente e as rotas; gera erros de conversão e inconsistência de design.

## Conclusão

Para este projeto, a melhor abordagem é usar UUID tanto na base de dados quanto nas URLs. Isso mantém a solução coerente, segura e alinhada com a arquitetura já adotada.
