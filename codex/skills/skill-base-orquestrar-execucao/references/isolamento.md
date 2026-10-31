# Isolamento e integração

Use o checkout existente quando permitir preservar trabalho e serializar edições com segurança. Antes de isolar ou retomar, confira `git status --short`, `git diff`, alterações staged e não rastreadas, e `git worktree list --porcelain`. Descubra a branch de integração; não presuma seu nome. Preserve índice e alterações de terceiros.

Se uma worktree for necessária, escolha um diretório reservado, resolva seu caminho absoluto e confira seus limites. Use uma branch livre conforme convenção local, com base identificada. Worktrees novas não herdam alterações locais: não copie o checkout inteiro nem caches. Materialize somente predecessores necessários, de origem conhecida, revisados e validados; se não puder separá-los, retenha o consumidor.

Registre a base efetiva de cada atribuição: commit e deltas necessários ainda não commitados, com arquivos e hashes quando isso for necessário para distinguir entregas. Inclua arquivos novos/não rastreados; `git diff` sozinho não os mostra. Atualize a base quando o predecessor mudar.

Antes da integração, congele a entrega e confira arquivos alterados, novos, removidos, renomeados e binários contra a base efetiva. Revise os trechos e efeitos semânticos; uma cópia de arquivo inteiro pode apagar mudanças intervenientes. Se houver sobreposição ou procedência incerta, preserve os dois trabalhos e resolva o trecho antes de integrar.

Integre serialmente e execute as provas pertinentes sobre a composição resultante. Só libere consumidores após essa verificação. Quando não houver commit, identifique a composição validada por base e deltas; um teste isolado antigo não comprova o estado atual.

Se commit estiver autorizado, selecione apenas o trabalho aceito e confira o índice sem desestagiar mudanças alheias. Caso não seja separável, registre commit pendente. Não force limpeza, reset ou reescrita de histórico para facilitar integração.

Na retomada, confronte branches, worktrees, processos ativos, reservas e fontes com o acompanhamento antes de criar recursos novos. Remova uma worktree somente quando não houver editor/processo ativo e todo trabalho exclusivo estiver comprovadamente preservado e integrado, inclusive arquivos ignorados necessários. Verifique seu caminho absoluto dentro da área reservada e use operações Git adequadas; não force remoção nem apague branches como efeito colateral.
