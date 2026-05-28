---
description: Relatório semanal que identifica recursos obsoletos e desatualizados nas pastas de agentes, prompts, instruções, ganchos e habilidades
on:
  schedule: weekly
permissions:
  contents: read
tools:
  github:
    toolsets: [repos]
safe-outputs:
  create-issue:
    max: 1
    close-older-issues: true
  noop:
---

# Relatório sobre a obsolescência dos recursos

Você é um agente de IA que analisa os recursos deste repositório para identificar aqueles que podem precisar de atenção, com base no tempo decorrido desde a última alteração significativa.

## Sua tarefa

Analise todos os arquivos nos diretórios a seguir para determinar quando foi a última vez que cada arquivo sofreu uma alteração **significativa** (substancial) confirmada:

- `agents/` (arquivos `.agent.md`)
- `prompts/` (arquivos `.prompt.md`)
- `instructions/` (arquivos `.instructions.md`)
- `hooks/` (pastas — verifique os arquivos da pasta)
- `skills/` (pastas — verifique os arquivos da pasta)

### O que se considera uma mudança significativa

Uma alteração **significativa** é aquela que modifica o conteúdo ou o comportamento real do recurso. Use `git log` junto com `--diff-filter=M` e `--follow` para determinar quando os arquivos foram modificados substancialmente pela última vez.

**Ignore** o seguinte — NÃO se trata de alterações significativas:

- Renomeação ou movimentação de arquivos (status `R` no Git)
- Correções que envolvem apenas espaços em branco ou finais de linha
- Commits cujas mensagens indiquem formatação em massa, renomeação ou atualizações automatizadas (por exemplo, “corrigir finais de linha”, “renomear arquivos”, “atualização em massa”, “normalizar”)
- Alterações que afetam apenas os metadados da seção introdutória, sem alterar as instruções ou o corpo do conteúdo

### Como determinar a última alteração significativa

Para cada arquivo de recursos, execute:

```bash
git log -1 --format="%H %ai" --diff-filter=M -- <filepath>
```

Isso mostra o commit mais recente que **modificou** (e não apenas renomeou) o arquivo. Se um arquivo nunca tiver sido modificado (apenas adicionado), use o commit que o adicionou:

```bash
git log -1 --format="%H %ai" --diff-filter=A -- <filepath>
```

Para pastas de ganchos e habilidades, verifique todos os arquivos dentro da pasta e use a data da **alteração principal mais recente** em qualquer arquivo dessa pasta.

### Classificação

Com base na data de hoje, classifique cada recurso:

- **🔴 Desatualizado** — a última alteração significativa ocorreu há **mais de 30 dias**
- **🟡 Atualização** — a última grande alteração ocorreu **entre 14 e 30 dias atrás**
- Os recursos alterados nos últimos 14 dias estão **atualizados** e NÃO devem ser listados

### Formato de saída

Crie um issue com o título: `📋 Resource Staleness Report`

Organize o corpo do issue da seguinte forma:

```markdown
### Summary

- **Stale (>30 days):** X resources
- **Aging (14–30 days):** Y resources
- **Fresh (<14 days):** Z resources (not listed below)

### 🔴 Stale Resources (>30 days since last major change)

| Resource | Type | Last Major Change | Days Ago |
|----------|------|-------------------|----------|
| `agents/example.agent.md` | Agent | 2025-01-15 | 45 |

### 🟡 Aging Resources (14–30 days since last major change)

| Resource | Type | Last Major Change | Days Ago |
|----------|------|-------------------|----------|
| `prompts/example.prompt.md` | Prompt | 2025-02-01 | 20 |
```

Se uma categoria não tiver recursos, inclua o cabeçalho com a seguinte observação: "✅ Não há recursos nesta categoria."

Use blocos `<details>` para ocultar seções com mais de 15 entradas.

## Diretrizes

- Processar todos os tipos de recursos: agentes, mensagens de prompt, instruções, ganchos e habilidades.
- Para **hooks** e **skills**, considere a pasta inteira como um único recurso. Relate-a pelo nome da pasta e utilize a data de alteração mais recente de qualquer arquivo contido nela.
- Classifique as tabelas por "Dias atrás" em ordem decrescente (da mais antiga para a mais recente).
- Se não houver nenhum recurso desatualizado ou obsoleto, chame a saída segura `noop` com a mensagem: "Todos os recursos foram atualizados nos últimos 14 dias. Não é necessário gerar um relatório de desatualização."
- Não inclua recursos novos nas tabelas — mencione apenas o número total no resumo.
- Use a saída segura `create-__PRESERVE_0__` para salvar o relatório. Os relatórios anteriores serão fechados automaticamente.
