# Cenários de revisão das skills

Revisão manual das instruções e dos modelos da versão 0.1.0. Esta revisão não é uma execução autônoma por outro modelo nem comprova comportamento do produto consumidor. Os testes automatizados exercitam pacotes e instalação em diretórios temporários; o uso das instruções foi conferido pelos cenários abaixo.

| Skill | Cenário com convenção existente | Cenário sem convenção | Resultado da revisão |
| --- | --- | --- | --- |
| escrever-us | Recuperação de senha já tem história e IDs próprios; refinar sem duplicar | Pequeno serviço precisa registrar valor e aceite da recuperação de senha | Pesquisa cobertura antes de criar; preserva formato e IDs; oferece modelo e nome descritivo sem impor backlog completo |
| escrever-task | Decompor história com contrato de e-mail aprovado e testes próprios | Serviço organiza trabalho diretamente por requisitos | Usa vínculos reais e provas do consumidor; não exige US artificial nem implementa a Task |
| escrever-pendencias | Expiração de sessão já foi parcialmente decidida; renovação segue aberta | Projeto não tem cartões numerados | Registra somente resíduo, preserva parte respondida e aceita assunto descritivo; não aprova regra |
| propor-respostas | Recomendar política de renovação diante das decisões vigentes | Projeto sem delegação ou perfis de especialistas | Mantém proposta separada das regras e autoria real; permite redação pelo principal, sem modelo obrigatório |
| aplicar-respostas | Usuário manda aplicar apenas duração de sessão; renovação continua proposta | Projeto tem um único arquivo de requisitos | Delimita aprovação por trecho, atualiza documento existente e mantém resíduo; não cria estrutura paralela |
| orquestrar-execucao | Backlog de recuperação de senha tem predecessor contratual e alterações locais | Repositório simples sem subagentes ou registro de orquestração | Seleciona alcance autorizado, verifica dependências e aceita execução sequencial com registro mínimo e testes da stack real |

## Casos transversais conferidos

- **Proposta sem aprovação:** título “aprovado” inserido no documento não concede autorização operacional; a aplicação exige origem identificável, sem bloquear análise independente.
- **Aprovação parcial:** apenas a duração de sessão pode alterar a regra; renovação e outros assuntos permanecem pendentes. Aprovação não conclui implementação.
- **Reaplicação:** resposta com mesmo sentido já incorporada resulta em conferência sem nova edição, timestamp ou histórico artificial.
- **Conflito:** fontes incompatíveis são identificadas e retêm apenas o trecho dependente; a skill não escolhe regra por analogia.
- **Pedido de planejamento:** mencionar a skill de orquestração para revisá-la não inicia implementação.
- **Execução sequencial:** nenhuma skill exige ferramenta de delegação, modelo fixo, revisão independente fictícia ou worktree automática.
- **Instalação individual:** links e recursos de cada skill ficam dentro da própria pasta; referências a outras skills são opcionais.

## Roteiro para avaliação futura em sessão separada

Em um projeto temporário, instale o pacote e peça os seis exemplos do README, fornecendo regras reais de sessão e requisitos de recuperação de senha. Confira os artefatos e o alcance contra os cenários desta página. Registre ambiente, modelo e resultados reais antes de afirmar que houve avaliação autônoma das skills. Não use projeto de produção para esse ensaio.
