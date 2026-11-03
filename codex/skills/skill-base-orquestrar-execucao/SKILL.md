---
name: skill-base-orquestrar-execucao
description: Executar ou retomar um backlog de software delimitado, verificando dependências e integrando entregas. Não inicia implementação quando o pedido é somente planejar.
---

# Orquestrar execução

Siga as instruções e convenções do projeto. Pesquise a documentação existente antes de criar novos registros. Preserve IDs, histórico e alterações alheias. Use os modelos abaixo apenas se o projeto não tiver formato próprio.

1. Identifique o escopo autorizado, o estado real das Tasks e as evidências dos predecessores. Não invente requisitos para liberar trabalho.
2. Selecione entregas elegíveis por dependências reais. Uma Task aceita pode liberar consumidores sem exigir o fechamento de toda a US.
3. Execute sequencialmente por padrão. Delegue quando permitido e útil, usando recursos disponíveis e arquivos exclusivos; serialize mudanças em contratos ou arquivos compartilhados.
4. Use worktrees apenas quando necessário ou solicitado. Identifique a base e os deltas necessários; não copie alterações alheias nem descarte trabalho para facilitar integração.
5. Revise e integre uma entrega por vez. Execute as verificações adequadas sobre a composição resultante antes de liberar consumidores. Build, testes e validação visual comprovam coisas diferentes.
6. Atualize o acompanhamento com resultados reais e próximo passo. Preserve histórico; conclua cada item pelo seu próprio aceite. Git e ações externas seguem a autorização vigente.
7. Continue dentro do escopo solicitado. Na retomada, confira o estado real antes de duplicar trabalho ou recursos.

Modelo para atribuição, quando necessário: [Entrega](assets/atribuicao.md).

Ao entregar, informe arquivos alterados, verificações realizadas e pendências. Editar esta skill não autoriza executar seu fluxo no consumidor.
