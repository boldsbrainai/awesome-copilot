---
name: "Learning Hub Updater"
description: "Verificar diariamente se há novos recursos e atualizações do GitHub Copilot. Abrir um PR caso o Learning Hub precise de atualização."
on:
  schedule: daily
  workflow_dispatch:
tools:
  bash: ["curl", "gh"]
  edit:
  web-fetch:
  github:
    toolsets: [repos]
safe-outputs:
  allowed-domains:
    - github.blog
    - code.visualstudio.com
    - nishanil.github.io
  create-pull-request:
    labels: [automated-update, copilot-updates]
    title-prefix: "[bot] "
    base-branch: staged
---

# Confira as incríveis atualizações do GitHub Copilot

Você é responsável pela manutenção da documentação do Awesome GitHub Copilot Learning Hub. Sua função é verificar se há atualizações recentes no GitHub Copilot e determinar se as páginas do Learning Hub no `website/learning-hub` precisam ser atualizadas.

## Passo 1 — Obter as atualizações mais recentes do Copilot

Use `web-fetch` para ler as páginas a seguir e extrair as entradas mais recentes dos últimos 7 dias:

- https://github.blog/changelog/label/copilot/ — registro oficial de alterações
- https://github.com/github/copilot-cli/blob/main/changelog.md — CLI: histórico de alterações
- https://github.blog/ai-and-ml/github-copilot/ — publicações no blog
- https://code.visualstudio.com/updates - Notas de lançamento do VS Code (filtrar atualizações relacionadas ao Copilot)
- https://nishanil.github.io/copilot-guide/ - guia mantido pela comunidade (verifique se há commits ou atualizações recentes)

Use também `gh` e CLI para verificar as versões e commits mais recentes no repositório `github/copilot-cli`.

Procure por:

- Novos recursos ou funcionalidades (novos comandos com barra, novos modos de agente, novas integrações)
- Alterações significativas em recursos existentes (mudanças de nome, descontinuação de recursos, anúncios de lançamento geral)
- Novas opções de personalização (instruções, agentes, habilidades, MCP, ganchos, plug-ins)
- Novos recursos da plataforma (memória, espaços, atualizações de SDK)
- Projetos comunitários de destaque desenvolvidos no Copilot

## Passo 2 — Compare com o Centro de Aprendizagem atual

Leia as páginas do Learning Hub atual e compare os recursos documentados nelas com o que você encontrou na Etapa 1, com exceção da seção `cli-for-beginners`, já que tratamos as atualizações dessa seção separadamente. Quaisquer alterações sugeridas para essas páginas serão rejeitadas.

Identifique:

- **Recursos ausentes** — novas funcionalidades ainda não documentadas
- **Informações desatualizadas** — recursos que foram renomeados, descontinuados ou sofreram alterações significativas
- **Links ausentes** — novos documentos oficiais ou publicações no blog que não constam na seção “Leitura adicional”

Se não houver novidades ou se tudo já estiver atualizado, pare por aqui e informe que não são necessárias atualizações.

## Etapa 3 — Atualizar o Centro de Aprendizagem

Se forem necessárias atualizações, decida se é preciso adicionar uma nova página (por exemplo, para um novo recurso importante) ou se as páginas existentes podem ser atualizadas com novas seções.

### Para novas páginas:

Deve-se criar uma nova página para os principais recursos ou funcionalidades que justifiquem uma documentação própria (por exemplo, um novo recurso do Copilot, um novo padrão de trabalho com o Copilot, etc.).

Para criar uma nova página:

1. Crie um novo arquivo Markdown na seção apropriada de `website/learning-hub` (por exemplo, `website/learning-hub/agents/new-agent.md`).
2. Escreva um resumo sobre o novo recurso, como ele funciona e seus casos de uso.
3. Adicione uma seção "Leitura complementar" com links para a documentação oficial, publicações em blogs e recursos relevantes da comunidade.

### Para atualizações em páginas existentes:

Se as novas informações puderem ser adicionadas às páginas existentes, edite essas páginas para incluir esclarecimentos, novas seções ou informações atualizadas, conforme necessário. Certifique-se de atualizar todos os links relevantes nas seções “Leitura complementar”.

## Passo 4 — Abra um pull request

Crie um pull request com suas alterações, usando o `staged` e o branch como base para o branch. O título do PR deve resumir o que foi atualizado (por exemplo, “Adicionar/planejar comando e documentação do modelo de marketplace”). O corpo do PR deve listar:

1. Quais novos recursos ou alterações foram identificados
2. Quais seções do guia foram atualizadas
3. Links para os comunicados originais

O PR deve ter como alvo os rótulos `staged` e branch e incluir os rótulos `automated-update` e `copilot-updates`.
