---
name: skill-base-escrever-pendencias
description: Registrar ou revisar dúvidas e lacunas de requisitos de software após pesquisar cobertura e decisões vigentes. Não aprova decisões, encerra dúvidas por recomendação ou implementa funcionalidades.
---

# Escrever pendências

Registre perguntas que ainda precisam de resposta, com impacto e fontes. Editar esta skill não autoriza criar pendências reais.

## Investigar antes de registrar

Leia instruções do consumidor e descubra sua fila canônica de dúvidas, decisões, requisitos e histórico. Pesquise pelo assunto e identificadores em registros ativos e encerrados. Consulte decisões posteriores e o trecho de requisito/implementação afetado. Ausência de código não é, por si só, lacuna de requisito.

Separe regra vigente, recomendação, decisão delegada e pergunta residual. Uma decisão parcial não fecha toda a dúvida e não reabre a parte respondida. Não converta uma autorização limitada em decisão sobre políticas não abrangidas.

Reutilize a pendência existente para o mesmo resíduo. Crie uma nova apenas quando a lacuna e ausência de cobertura estiverem demonstradas. Respeite a convenção local de IDs; sem convenção, use nome descritivo. Não crie um ID de decisão para registrar uma pergunta.

## Escrever e relacionar

Preserve o formato local ou adapte [o modelo de pendência](assets/modelo-pendencia.md).

- Expresse uma pergunta delimitada e o que já está definido, com fontes verificáveis.
- Apresente alternativas viáveis e, quando houver fundamento, uma recomendação explicitamente proposta.
- Explique impacto para o usuário e consumidores técnicos, requisitos/Tasks relacionados e qual saída depende da resposta.
- Mantenha uma fila canônica, com índices apontando para ela, sem duplicar cartões.

Não aprove regras, encerre perguntas por recomendação nem implemente código neste fluxo. Alterações de backlog solicitadas devem seguir suas convenções; se as skills de US/Task estiverem disponíveis, podem auxiliar, mas não são dependências desta skill.

## Conferir e entregar

Verifique fontes posteriores, cobertura pesquisada, links e coerência entre parcela definida e pergunta residual. Atualize somente índices afetados pelo mecanismo existente; execute verificações documentais incidentes, se disponíveis. Não invente scripts ausentes nem faça build para provar escrita documental.

Entregue fontes, arquivos, alternativas e trecho bloqueado com VERIFICADO, NÃO EXECUTADO ou BLOQUEADO, descrevendo comando e resultado quando aplicável. A recomendação permanece proposta; decisões exigem a origem de autorização correspondente.
