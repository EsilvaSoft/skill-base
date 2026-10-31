# Skill Base

Skills reutilizáveis em português para análise e desenvolvimento de software. Projeto open source da **EsilvaSoft**, sob a [licença MIT](LICENSE).

O catálogo adapta fluxos do Xenogenesis sem depender de suas regras, tecnologias ou organização. Cada skill descobre as convenções do projeto consumidor e preserva a distinção entre proposta, decisão, implementação e evidência. Consulte a [procedência](PROVENANCE.md).

## Agentes e catálogo

| Agente | Suporte |
| --- | --- |
| Codex | Disponível: seis skills, instalação e artefatos de release |
| Claude | Estrutura reservada; ainda sem implementação |
| GitHub Copilot | Estrutura reservada; ainda sem implementação |

| Skill | Finalidade |
| --- | --- |
| `skill-base-escrever-us` | Histórias com valor, escopo e critérios verificáveis |
| `skill-base-escrever-task` | Entregas técnicas com dependências e aceite |
| `skill-base-escrever-pendencias` | Dúvidas residuais com fontes, alternativas e impactos |
| `skill-base-propor-respostas` | Recomendações documentais para revisão |
| `skill-base-aplicar-respostas` | Incorporação documental de respostas autorizadas |
| `skill-base-orquestrar-execucao` | Execução de backlog delimitado e integração verificada |

As skills podem ser instaladas individualmente; nenhuma depende de outra. Não há skill de balanceamento ou calibração.

## Instalar no Codex

Requisitos: **Python 3.10+**, Codex e uma ferramenta para extrair ZIP. O instalador não usa bibliotecas externas, rede ou credenciais. No Windows, use `py` no lugar de `python` se esse for o comando disponível.

1. Abra [Releases](https://github.com/EsilvaSoft/skill-base/releases) e escolha uma versão explícita, por exemplo `v0.1.0`.
2. Baixe `skill-base-codex-v0.1.0.zip` e `SHA256SUMS`. Para uma única skill, baixe seu ZIP individual na mesma release.
3. Confira o SHA-256 do ZIP contra a linha de mesmo nome em `SHA256SUMS`, **antes de extrair ou executar o instalador**. O manifesto confere integridade interna, mas não substitui a conferência do arquivo baixado de uma fonte confiável.

PowerShell:

```powershell
Get-FileHash .\skill-base-codex-v0.1.0.zip -Algorithm SHA256
Get-Content .\SHA256SUMS
Expand-Archive .\skill-base-codex-v0.1.0.zip -DestinationPath .\extraido
```

Linux:

```sh
sha256sum skill-base-codex-v0.1.0.zip
cat SHA256SUMS
unzip skill-base-codex-v0.1.0.zip -d extraido
```

Os exemplos abaixo partem da pasta extraída `skill-base-codex-v0.1.0`, que contém `install.py`, `manifest.json` e `skills/`. Ajuste a versão e os caminhos ao pacote escolhido. As primeiras releases só estarão disponíveis depois de o mantenedor publicar uma tag no GitHub.

### Instalação por projeto

Informe explicitamente a raiz de um projeto existente. As skills serão copiadas para `<projeto>/.agents/skills/`:

```sh
python install.py --project "/caminho/meu projeto" --all
```

No Windows:

```powershell
python .\install.py --project "C:\projetos\Meu Projeto" --all
```

Para selecionar uma ou várias skills do pacote:

```sh
python install.py --project "/caminho/meu projeto" --skill skill-base-escrever-us --skill skill-base-escrever-task
```

Em um ZIP individual, `--all` instala apenas a skill incluída nele. Você também pode executar o instalador do checkout com `python tools/install.py --source "/pasta/do/pacote/extraido" --project "/caminho/meu projeto" --all`.

### Instalação global

Para disponibilizar as skills em todos os seus projetos:

```sh
python install.py --global --all
```

O destino é `~/.agents/skills/` (`$HOME\.agents\skills` no PowerShell). Os destinos por projeto e usuário seguem a [documentação oficial do Codex](https://learn.chatgpt.com/docs/build-skills). Evite instalar a mesma skill nos dois escopos: nomes iguais não são mesclados e podem aparecer duplicados.

O instalador exige escolha explícita de escopo e seleção, verifica os arquivos do pacote e recusa colisões. Cada skill instalada recebe também a licença MIT, preservando o aviso ao reutilizá-la em outros projetos. O Codex detecta as skills automaticamente; reinicie se elas não aparecerem. A seleção automática fica habilitada e a invocação explícita usa `$nome-da-skill`.

### Atualizar ou remover

Baixe e confira o novo pacote. Execute seu instalador com `--replace` para substituir **somente as skills selecionadas**:

```sh
python install.py --project "/caminho/meu projeto" --skill skill-base-escrever-us --replace
```

Faça backup de personalizações antes de substituir: a pasta da skill selecionada será trocada integralmente, removendo também recursos antigos. Outras skills e arquivos do projeto são preservados. Para atualizar todas as skills daquele pacote, use `--all --replace`. A versão efetivamente instalada pode ser rastreada pela versão do pacote usado; os arquivos instalados permanecem o formato nativo de skill do Codex.

Para remover, apague apenas a pasta da skill no escopo em que ela foi instalada. Por exemplo, no PowerShell, a partir da raiz do projeto:

```powershell
Remove-Item -LiteralPath ".agents/skills/skill-base-escrever-us" -Recurse
```

No Linux, na mesma raiz:

```sh
rm -r -- .agents/skills/skill-base-escrever-us
```

## Usar

Exemplos de pedidos após instalar:

```text
Use $skill-base-escrever-us para refinar a história de recuperação de senha,
preservando o formato e os identificadores do nosso backlog.

Use $skill-base-escrever-task para decompor essa história em entregas verificáveis.
Não implemente as funcionalidades nesta etapa.

Use $skill-base-escrever-pendencias para registrar as dúvidas residuais de expiração
de sessão, após conferir as decisões existentes.

Use $skill-base-propor-respostas para recomendar respostas às dúvidas de sessão.
Mantenha as recomendações como propostas para revisão.

Use $skill-base-aplicar-respostas para incorporar apenas a resposta sobre duração
da sessão que aprovei neste pedido; a política de renovação continua pendente.

Use $skill-base-orquestrar-execucao para executar as Tasks de recuperação de senha
que especifiquei. Trabalhe sequencialmente, preserve alterações locais e use os
comandos de teste deste projeto.
```

Os modelos incluídos servem a projetos sem formato próprio. As skills não exigem uma estrutura de backlog, framework, modelo de IA ou subagentes específicos. Autorizações e instruções vigentes do projeto consumidor continuam determinando o alcance do trabalho.

## Versionamento e desenvolvimento

`VERSION` define uma versão SemVer única para todo o catálogo, inicialmente `0.1.0`. Todos os ZIPs de uma release compartilham a versão. Mudanças incompatíveis em invocação, instalação ou comportamento exigem major; novas capacidades compatíveis, minor; correções, patch.

Estrutura: `codex/skills/` contém as skills; `claude/` e `github-copilot/` reservam suporte futuro; `tools/` contém validação, empacotamento e instalação; `tests/` contém testes das ferramentas e cenários de revisão.

Na raiz do checkout:

```sh
python -m pip install -r requirements-dev.txt
python tools/validate.py
python -m unittest discover -s tests -v
python tools/package.py
```

Os artefatos ficam em `dist/`, ignorado pelo Git. Para testar a instalação sem release publicada, extraia o ZIP gerado e siga os mesmos passos acima. Builds sem commit inicial registram `source_commit: "uncommitted"`; em releases, o manifesto registra o commit da tag. Os hashes identificam os bytes efetivamente empacotados.

Uma tag enviada ao GitHub no formato exato `vX.Y.Z`, correspondente a `VERSION`, dispara validação e testes Windows/Linux antes da publicação. A release contém um ZIP completo, seis individuais, um manifesto externo e `SHA256SUMS`. Cada ZIP também inclui manifesto, licença, procedência e instalador. Claude e Copilot ficam fora dos pacotes.

O workflow cria rascunho, anexa artefatos e publica após sucesso. Releases existentes não são sobrescritas. Veja [contribuição e publicação](CONTRIBUTING.md) e os [cenários de revisão das skills](tests/skill-scenarios.md).
