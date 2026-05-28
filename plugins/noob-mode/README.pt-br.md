# Plugin Noob Mode

Camada de tradução em linguagem simples para usuários não técnicos do Copilot CLI. Quando ativado, o Copilot traduz automaticamente cada solicitação de permissão, mensagem de erro e saída técnica para uma linguagem clara, sem jargões, com indicadores de risco codificados por cor.

## Para quem é isto?

Qualquer pessoa que use o Copilot CLI, mas **não** seja desenvolvedora de software:
- Advogados e profissionais da área jurídica
- Gerentes de produto e gerentes de programa
- Stakeholders de negócio e executivos
- Redatores técnicos e criadores de conteúdo
- Designers que trabalham com ferramentas adjacentes a código
- Qualquer pessoa que esteja começando na linha de comando

## Instalação

```bash
copilot plugin install noob-mode@awesome-copilot
```

## O que está incluído

### Comandos (comandos slash)

| Comando | Descrição |
|---------|-------------|
| `/noob-mode:noob-mode` | Ativa o Noob Mode para a sessão atual. O Copilot explicará tudo em linguagem simples — cada ação, cada solicitação de permissão e cada resultado. |

### Ativos incluídos

| Ativo | Descrição |
|-------|-------------|
| `references/glossary.md` | Mais de 100 termos técnicos definidos em linguagem simples, organizados por categoria (Git, Sistema de Arquivos, Desenvolvimento, Web, Copilot CLI) |
| `references/examples.md` | 15 exemplos de antes/depois mostrando como o Noob Mode transforma saída técnica em explicações claras |

## Recursos

| Recurso | O que isso significa para você |
|---|---|
| **Tradução de aprovação** | Toda vez que o Copilot pede permissão, ele explica O QUE quer fazer, POR QUÊ, quão ARRISCADO é e o que acontece se você disser sim ou não |
| **Indicadores de risco** | Níveis de risco codificados por cor (🟢 Baixo, 🟡 Moderado, 🔴 Alto, ⛔ Crítico) para que você veja instantaneamente se uma ação é segura |
| **Detecção de jargão** | Termos técnicos são definidos automaticamente em linguagem simples na primeira vez em que aparecem |
| **Planos passo a passo** | Tarefas com várias etapas começam com um roteiro em linguagem simples para que você saiba o que vem a seguir |
| **Tradução de saída** | Mensagens de erro e resultados de comandos são traduzidos para “aqui está o que isso significa” |
| **Resumos de conclusão** | Após cada tarefa, você recebe um resumo do que mudou, do que foi criado e de como desfazer |
| **Suporte à decisão** | Quando você precisa escolher entre opções, cada uma é explicada com trade-offs e uma recomendação |

## Exemplo

**Sem Noob Mode:**
```
Allow tool: bash with command "grep -r 'indemnification' ./contracts/"?
[y/n]
```

**Com Noob Mode:**
```
📋 O QUE ESTOU PEDINDO PARA FAZER:
Quero pesquisar em todos os arquivos da sua pasta "contracts" pela palavra "indemnification".

🎯 POR QUÊ:
Você me pediu para encontrar toda menção a indemnification em seus contratos.

⚠️ RISCO: 🔴 Alto (mas seguro neste caso)
Executar comandos geralmente é de alto risco, mas este apenas pesquisa — ele não
altera nem exclui nada.

✅ Se você aprovar: mostrarei cada arquivo em que "indemnification" aparece.
❌ Se você recusar: posso ler os arquivos um por um, mas isso levará mais tempo.
```

## Como desativar

Diga "turn off noob mode" na sua conversa, e o Copilot retornará ao estilo de comunicação padrão.

## Origem

Este plugin faz parte do [Awesome Copilot](https://github.com/github/awesome-copilot), uma coleção orientada pela comunidade de extensões do GitHub Copilot.

## Licença

MIT
