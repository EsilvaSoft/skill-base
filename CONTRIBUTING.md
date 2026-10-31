# Contribuir e manter

Use Python 3.10 ou superior. Na raiz:

```sh
python -m pip install -r requirements-dev.txt
python tools/validate.py
python -m unittest discover -s tests -v
python tools/package.py
```

Cada skill é autocontida: `SKILL.md`, `agents/openai.yaml` e somente os modelos/referências necessários. Não dependa da instalação de outra skill. Use nomes `skill-base-<ação>`, descrições discriminantes e links relativos verificáveis. Adapte-se às convenções do consumidor em vez de impor o layout deste repositório. Novas skills precisam de cenários de uso e revisão de seus limites de atuação.

## Versões

`VERSION` é a única versão do catálogo, no formato `X.Y.Z`, sem zeros à esquerda. Todos os pacotes de uma release usam a mesma versão, mesmo quando apenas uma skill mudou. Incremente major para mudanças incompatíveis em nomes, instalação ou comportamento; minor para capacidades novas compatíveis; patch para correções. Essa política também se aplica à série `0.x`.

Atualize `VERSION` e `CHANGELOG.md` antes da tag. Preserve nomes de skills como interface pública; uma renomeação afeta invocações e pastas instaladas. Não inclua metadados de versão independentes em cada skill.

## Publicar

Após integrar e validar a alteração no GitHub, o mantenedor cria e envia uma tag, por exemplo:

```sh
git tag -a v0.1.0 -m "Skill Base 0.1.0"
git push origin v0.1.0
```

O workflow confere a tag contra `VERSION`, executa os testes em Windows/Linux e gera os artefatos a partir do commit marcado. Cria um rascunho, anexa os arquivos e só então o publica. Tags inválidas ou divergentes falham antes da publicação. O token padrão do Actions precisa de `contents: write` no job de publicação.

Uma release já publicada nunca é substituída pelo workflow. Em caso de falha durante o upload, o rascunho fica para inspeção; remova apenas o rascunho incompleto antes de repetir o job. Uma correção em conteúdo já publicado exige nova versão e nova tag. Não mova tags publicadas.

Se uma falha na infraestrutura do workflow impedir a publicação antes de criar a release, corrija o workflow na branch padrão e use a execução manual **Validate and release**, informando a tag existente. A execução usa o workflow corrigido, mas faz checkout e valida o conteúdo da tag solicitada, sem movê-la:

```sh
gh workflow run ci.yml --ref master -f tag=v0.1.0
```

Substitua `master` pela branch padrão efetiva do repositório. A execução manual mantém as mesmas verificações de versão, testes Windows/Linux e recusa de releases existentes.

O destino é obtido de `GITHUB_REPOSITORY`; o endereço documentado é `EsilvaSoft/skill-base`. A criação do remoto e o primeiro push são operações do mantenedor, separadas da implementação local.
