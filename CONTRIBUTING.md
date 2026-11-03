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

`VERSION` é a única versão do catálogo, no formato `X.Y.Z`, sem zeros à esquerda. Todos os pacotes gerados usam a mesma versão, mesmo quando apenas uma skill mudou. Incremente major para mudanças incompatíveis em nomes, instalação ou comportamento; minor para capacidades novas compatíveis; patch para correções. Essa política também se aplica à série `0.x`.

Mantenha `VERSION` e `CHANGELOG.md` coerentes com as alterações do catálogo. Preserve nomes de skills como interface pública; uma renomeação afeta invocações e pastas instaladas. Não inclua metadados de versão independentes em cada skill.

## Pacotes locais e CI

Gere os pacotes localmente quando precisar instalar ou compartilhar o catálogo:

```sh
python tools/package.py
```

Os arquivos ficam em `dist/`, incluindo os ZIPs, o manifesto e `SHA256SUMS`. A versão vem de `VERSION`; a geração dos pacotes não depende de uma tag Git.

O workflow executa validação, testes e empacotamento em Windows/Linux nos pushes de branches, pull requests ou execução manual. Ele tem somente permissão de leitura e não publica no GitHub Releases. O projeto não define um fluxo de publicação automática.
