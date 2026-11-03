# Skill Base

Seis skills em português para análise e desenvolvimento de software com Codex. Adaptadas do [Xenogenesis](https://github.com/EsilvaSoft/Xenogenesis), com instruções genéricas e reutilizáveis.

| Skill | Uso |
| --- | --- |
| `skill-base-escrever-us` | Escrever User Stories com valor e critérios de aceite |
| `skill-base-escrever-task` | Especificar tarefas com dependências e verificações |
| `skill-base-escrever-pendencias` | Registrar dúvidas de requisitos |
| `skill-base-propor-respostas` | Propor respostas para revisão |
| `skill-base-aplicar-respostas` | Incorporar respostas autorizadas na documentação |
| `skill-base-orquestrar-execucao` | Executar um backlog delimitado e integrar entregas |

## Instalação

Baixe ou clone este repositório. Copie as pastas desejadas de `codex/skills/` para:

- **Projeto:** `<projeto>/.agents/skills/`
- **Todos os projetos:** `~/.agents/skills/`

Copie cada pasta inteira, incluindo `SKILL.md`, `agents/` e `assets/`. Cada skill é independente e não exige Python ou bibliotecas adicionais. Ao redistribuir as skills, inclua também o arquivo `LICENSE` deste repositório.

Para atualizar, substitua a pasta da skill, preservando antes suas personalizações. Para remover, apague essa pasta. Se o Codex não detectar a mudança, reinicie-o.

## Uso

Peça diretamente, por exemplo:

```text
Use $skill-base-escrever-us para descrever a recuperação de senha.
Use $skill-base-escrever-task para decompor essa história em tarefas.
Use $skill-base-orquestrar-execucao para executar as tarefas selecionadas.
```

O Codex também pode selecionar uma skill automaticamente conforme o pedido. As instruções se adaptam às convenções do projeto; os modelos são opcionais.

## Licença

[MIT](LICENSE) — EsilvaSoft.
