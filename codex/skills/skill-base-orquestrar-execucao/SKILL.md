---
name: skill-base-orquestrar-execucao
description: Executar ou retomar um backlog de software delimitado, selecionando Tasks elegíveis, coordenando dependências e integrando entregas verificadas. Não inicia execução quando o pedido é apenas planejar ou revisar a skill.
---

# Orquestrar execução

Selecione, execute, acompanhe e integre o trabalho solicitado. O pedido define o limite: criar esta skill, escrever planejamento ou analisar backlog não autoriza implementá-lo. Respeite políticas de execução, Git e ações externas do consumidor.

## Descobrir o estado e escolher trabalho

Leia instruções do projeto, backlog incidente, decisões, código e evidências necessárias. Descubra convenções de acompanhamento, comandos de validação e limites de ferramentas. Não presuma tecnologia, branch principal, número de agentes ou modelo.

Com IDs ou objetivo delimitado, mantenha esse recorte. Quando houver autorização para avançar um backlog, priorize predecessores que liberem entregas integráveis, sem implementar itens fora do alcance. Prontidão exige evidência atual: posição em onda, status histórico ou documento aprovado não comprovam predecessor implementado.

Verifique dependências por saída: entrega anterior aceita, contrato estável ou integração a validar antes do aceite. Uma Task aceita pode liberar consumidor sem exigir fechamento de toda a história fornecedora. Lacuna de requisito bloqueia apenas o comportamento dependente; não invente uma regra para liberá-lo.

## Executar e coordenar

Execute sequencialmente quando suficiente ou quando delegação não estiver autorizada/disponível. Se houver benefício e autorização, use subagentes reais, herdando limites e escolhendo capacidades disponíveis conforme a tarefa. Não exija modelos fixos nem crie chats do usuário para simular especialistas.

Antes de paralelizar, comprove arquivos exclusivos, contratos estáveis e responsável por compartilhados. Worktrees não garantem independência semântica; use-as apenas se necessário para isolamento ou se solicitado. Para esse caso, leia [isolamento e integração](references/isolamento.md).

Adapte [a atribuição](assets/atribuicao.md) para fornecer objetivo, fontes, base, predecessores comprovados, arquivos, aceite e verificações. Cada executor preserva trabalho alheio e retorna mudanças e evidências; mudanças de escopo ou contratos compartilhados exigem recoordenação antes de continuar.

Mantenha o acompanhamento canônico existente com estado real, reservas quando houver, resultados e próximo passo. Sem acompanhamento, use um registro mínimo adequado ao projeto; não duplique o backlog. Serialize edições e testes que compartilhem arquivos, saídas, portas ou outros recursos.

## Revisar, integrar e retomar

Revise o delta e os critérios, com revisão independente quando disponível e proporcional ao trabalho. Informe quando só houve autorrevisão; não finja aprovação independente. Integre uma entrega compatível por vez e valide a composição resultante antes de liberar consumidores.

Escolha provas pelos critérios e stack reais. Build, testes unitários, integração e validação visual são evidências diferentes. Falha na integração mantém a entrega pendente mesmo que o teste isolado tenha passado. Preserve o trabalho para correção localizada.

Conclua Tasks e histórias somente pelo aceite próprio, preservando histórico. Commit ou publicação seguem a autorização vigente, sem incorporar alterações alheias por conveniência. Não estabeleça autorização automática por US concluída.

Após cada entrega, reavalie elegibilidade e continue no alcance autorizado. Se nada estiver liberado ou a sessão precisar encerrar, registre bloqueios, composição validada, trabalho em curso e próximo passo. Na retomada, confronte registro e estado real antes de duplicar agentes, branches ou alterações. Não crie automações por mera pausa operacional.

Entregue IDs/objetivo, arquivos, decisões, revisão real, verificações e pendências com VERIFICADO, NÃO EXECUTADO e BLOQUEADO. Não declare todo o backlog concluído por encerrar uma rodada.
