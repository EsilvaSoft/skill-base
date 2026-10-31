---
name: skill-base-escrever-task
description: Criar ou decompor Tasks de software com entrega executável, dependências, aceite e verificações. Usar para especificar trabalho técnico; não para executá-lo ou substituir o valor da User Story.
---

# Escrever Tasks

Produza a especificação de uma entrega delimitada. Criar ou revisar esta skill não autoriza executar trabalho no consumidor.

## Identificar o delta

Leia as instruções do consumidor, requisito ou US relacionada, decisões, implementação pertinente e evidências dos predecessores. Descubra convenções de backlog, IDs, arquivos e validadores; não presuma tecnologia ou estrutura de pastas.

Pesquise cobertura por requisito e identificadores. Refine a Task responsável pelo mesmo delta; crie apenas lacunas comprovadas. Preserve IDs, aliases e histórico. Siga a política local de atribuição de IDs e confira reservas antes de escrever. Se não houver convenção, use nome descritivo sem inventar numeração.

Vincule uma US real quando o projeto exigir esse vínculo. Sem história adequada, registre a lacuna e redija a US somente se o pedido também a abranger. Projetos que organizam Tasks diretamente por requisito não precisam ganhar uma camada artificial de histórias.

## Especificar a entrega

Use o formato existente; na ausência dele, adapte [o modelo de Task](assets/modelo-task.md).

- Defina objetivo, fonte, entradas, saídas, escopo e exclusões, contratos incidentes e critérios de conclusão.
- Separe refinamento, implementação e integração quando tiverem entregas e aceites distintos; não imponha quantidade de Tasks nem testes como itens separados sem necessidade.
- Declare predecessores por recorte: entrega anterior, contrato estabilizado ou integração necessária antes do aceite. Justifique independência; ordem em uma lista não prova dependência nem prontidão.
- Identifique áreas candidatas e recursos compartilhados sem fingir que a especificação já reservou arquivos para um executor.
- Defina provas compatíveis com o comportamento: revisão documental, testes unitários, integração, interface visual ou outras verificações do consumidor. Não confunda build com teste, nem teste sem interface com validação visual.

Não invente requisito, contrato ou valor para liberar a entrega. Diferencie proposta, decisão vigente, definição delegada e lacuna essencial. Uma lacuna retém somente a saída dependente, com fonte e impacto registrados.

## Acompanhar e verificar

Task nova começa aberta. Preserve prontidão histórica, fase e conclusão como informações distintas. Ao reabrir trabalho concluído, registre motivo, aceite anterior e novo delta. Não registre verificações futuras como executadas nem herde conclusão de outro item.

Atualize vínculos afetados no requisito/US, índices e dependências existentes. Confira reciprocidade, unicidade e ausência de ciclos; não remova dependências para passar validação. Descubra e execute somente verificações documentais pertinentes à escrita da Task. Preserve falhas preexistentes separadas das introduzidas.

Entregue arquivos, fontes, decisões e verificações com comando, ambiente e resultado, usando VERIFICADO, NÃO EXECUTADO e BLOQUEADO. Especificação não implementa a entrega nem autoriza commit, publicação ou execução do backlog.
