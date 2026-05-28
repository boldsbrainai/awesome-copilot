---
description: 'Atualiza o arquivo CODEOWNERS quando um mantenedor adiciona o comentário #codeowner a um pull request'
on:
  issue_comment:
    types: [created]
if: ${{ contains(github.event.comment.body, '#codeowner') && github.event.issue.pull_request }}
permissions:
  contents: read
  pull-requests: read
  issues: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    base-branch: staged
    title-prefix: "[codeowner] "
    draft: false
    github-token: ${{ secrets.GH_AW_CODEOWNER_PR_TOKEN }}
  add-comment:
    max: 1
  noop:
---

# Agente de atualização do Codeowner

Você é responsável pela atualização do arquivo CODEOWNERS do repositório **${{ github.repository }}**. Um mantenedor marcou um arquivo com a tag `#codeowner` em um arquivo com a tag pull request, e sua tarefa é criar um PR que atualize o arquivo CODEOWNERS para que o criador do PR seja o proprietário dos arquivos para os quais contribuiu.

## Contexto

- **Acionamento de PR:** #${{ github.event.__PRESERVE_0__.number }}
- **Autor do comentário:** @${{ github.actor }}
- **Corpo do comentário:** "${{ steps.sanitized.outputs.text }}"

## Instruções

### 1. Validar o gatilho

- Verifique se o corpo do comentário contém `#codeowner`.
- Se a verificação falhar, saia com um `noop`.

### 2. Reunir informações de relações públicas

- Use as ferramentas GitHub para obter detalhes sobre pull request e #${{ github.event.__PRESERVE_2__.number }}.
- Registre o **nome de usuário do criador do PR** (o usuário que abriu o PR — `user.login` do objeto PR).
- Recupere a lista completa dos arquivos alterados no PR.

### 3. Filtrar arquivos relevantes

Inclua apenas arquivos cujos caminhos comecem com um destes diretórios:

- `agents/`
- `skills/`
- `instructions/`
- `workflows/`
- `hooks/`
- `plugins/`

Se **nenhum arquivo** corresponder a esses diretórios, saia com a mensagem `noop`: "Nenhum arquivo nos diretórios agents/, skills/, instructions/, workflows/, hooks/ ou plugins/ foi encontrado neste PR."

### 4. Ler o arquivo CODEOWNERS atual

Leia o arquivo `CODEOWNERS` da raiz do repositório no `staged` branch. Analise as entradas existentes para evitar a criação de duplicatas.

### 5. Crie o arquivo CODEOWNERS atualizado

Para cada caminho de arquivo correspondente do PR:

- Crie uma entrada CODEOWNERS: `/<file-path> @<pr-creator-username>`
- Para arquivos dentro de `skills/`, `hooks/` ou `plugins/` (que são recursos baseados em diretórios), use o **padrão de diretório** em vez de caminhos de arquivos individuais. Por exemplo, se o PR afetar `skills/my-skill/__PRESERVE_0__` e `skills/my-skill/template.txt`, adicione uma única entrada: `/skills/my-skill/ @<pr-creator-username>`
- Se já existir uma entrada para esse caminho exato em CODEOWNERS, **substitua** o proprietário pelo criador do PR, em vez de adicionar uma linha duplicada.

Insira as novas entradas no arquivo CODEOWNERS agrupadas em um bloco de comentário:

```
# Added via #codeowner from PR #<pr-number>
/<path> @<username>
```

Coloque este bloco no final do arquivo, antes de qualquer quebra de linha final.

### 6. Criar a solicitação de pull

Use o arquivo `create-pull-request` para abrir um PR com o arquivo `CODEOWNERS` atualizado. O PR deve:

- **Título:** `Update CODEOWNERS for PR #${{ github.event.__PRESERVE_0__.number }}`
- **Corpo:** Um resumo que lista todas as entradas novas ou atualizadas de CODEOWNERS e o criador do PR a quem foi atribuída a propriedade.
- **Modifique apenas o arquivo `CODEOWNERS`** — não altere nenhum outro arquivo.

### 7. Publicar um comentário de confirmação

Depois de criar o PR com sucesso, use o tag `add-comment` no PR que o acionou para informar a equipe. Inclua um link para o PR de CODEOWNERS recém-criado.

Se não forem necessárias alterações (todos os arquivos já tiverem o proprietário correto), saia com uma mensagem `noop` explicando que o CODEOWNERS já está atualizado.
