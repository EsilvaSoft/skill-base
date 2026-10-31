# Manutenção do Skill Base

Este repositório distribui skills; editar uma skill não autoriza executar seu fluxo no projeto consumidor. Mantenha conteúdo em português, genérico para análise e desenvolvimento de software. Não introduza modelos obrigatórios, tecnologias, caminhos de projetos ou autorizações Git herdadas das fontes.

Cada skill em `codex/skills/` deve poder ser instalada isoladamente, incluindo seus recursos e metadados. Preserve descoberta automática. Claude e GitHub Copilot estão reservados para trabalho futuro.

Para alterações no catálogo ou ferramentas, execute `python tools/validate.py`, `python -m unittest discover -s tests -v` e `python tools/package.py`. Dependências de manutenção estão em `requirements-dev.txt`. Não publique, envie tags ou configure remotos como efeito de manutenção local.
