---
description: Análise semanal de agentes, instruções e competências para identificar possíveis recursos duplicados e encaminhá-los para análise
on:
  schedule: weekly
permissions:
  contents: read
  issues: read
tools:
  github:
    toolsets: [repos, issues]
safe-outputs:
  create-issue:
    max: 1
    close-older-issues: true
    labels:
      - duplicate-review
  noop:
---

# Detector de recursos duplicados

Você é um agente de IA que analisa os recursos deste repositório para identificar possíveis duplicatas — recursos que parecem ter a mesma finalidade ou uma finalidade muito semelhante.

## Sua tarefa

Analise todos os recursos nos diretórios a seguir e identifique grupos de recursos que possam ser duplicados ou quase duplicados com base em seu **nome**, **descrição** e **conteúdo**:

- `agents/` (arquivos `.agent.md`)
- `instructions/` (arquivos `.instructions.md`)
- `skills/` (pastas — verifique se há `__PRESERVE_0__` dentro de cada uma)

### Passo 1: Reunir os metadados dos recursos

Para cada recurso, extraia:

1. **Nome do arquivo** (o caminho)
2. **Campo `description` na seção introdutória**
3. Campo **Front matter `name`** (se houver)
4. **Primeiras ~20 linhas do corpo do texto** (o Markdown após os dados preliminares)

Use o bash para ler arquivos com eficiência. Para saber mais sobre as técnicas, leia `skills/<name>/__PRESERVE_0__`.

### Passo 2: Identificar possíveis duplicatas

Compare os recursos e sinalize os grupos que pareçam ser possíveis duplicatas. Considere os recursos como possíveis duplicatas quando eles apresentarem **dois ou mais** dos seguintes sinais:

- **Nomes semelhantes** — nomes de arquivos ou campos `name` que compartilham termos-chave (por exemplo, `react-testing.agent.md` e `react-unit-testing.agent.md`)
- **Descrições semelhantes** — descrições que se referem à mesma tarefa, tecnologia ou área, com apenas pequenas diferenças de redação
- **Sobreposição de escopo** — recursos que se destinam à mesma linguagem/estrutura/ferramenta e à mesma atividade (por exemplo, duas instruções distintas sobre “melhores práticas de Python”)
- **Sobreposição entre elementos** — um agente e uma instrução (ou uma instrução e uma habilidade) que abordam o mesmo tema de forma tão completa que um pode tornar o outro supérfluo

Seja pragmático. Recursos que abordam temas relacionados, mas distintos, NÃO são duplicados. Por exemplo:
- `react.instructions.md` (padrões gerais de codificação do React) e `react-testing.agent.md` (agente de testes do React) **não** são duplicatas — elas têm finalidades diferentes.
- `python-fastapi.instructions.md` e `python-flask.instructions.md` **não** são duplicatas — elas se destinam a estruturas diferentes.
- `code-review.agent.md` e `code-review.instructions.md`, que realizam o mesmo tipo de revisão de código, **são** possíveis duplicatas que devem ser sinalizadas.

### Etapa 3: Verifique se há duplicatas conhecidas e aceitas

Antes de finalizar o relatório, procure por **versões anteriores do issue** marcadas como `duplicate-review` neste repositório:

```
Search for issues with label "duplicate-review" that are closed
```

Leia os comentários e o corpo desses issue anteriores para identificar quaisquer pares ou grupos que os revisores tenham marcado explicitamente como **"aceitos"** ou **"não duplicados"**. Procure por frases como:
- "aceito no estado em que se encontra"
- "sem duplicatas"
- "separar intencionalmente"
- "fique com os dois"
- itens marcados da lista de tarefas (ou seja, `- [x]`)

Exclua esses pares já aceitos do relatório atual. Se você incluir um grupo que já foi analisado anteriormente, acrescente uma nota: `(previously reviewed — see #<__PRESERVE_0__-number>)`.

### Etapa 4: Gerar o relatório

Crie um arquivo chamado issue com o nome: `🔍 Duplicate Resource Review`

Formate o corpo do texto da seguinte maneira:

```markdown
### Summary

- **Potential duplicate groups found:** N
- **Resources involved:** M
- **Known accepted (excluded):** K pairs from previous reviews

### How to Use This Report

Review each group below. If the resources are intentionally separate, check the box to mark them as accepted. These will be excluded from future reports.

### Potential Duplicates

#### Group 1: <Short description of what they share>

- [ ] Reviewed — these are intentionally separate

| Resource | Type | Description |
|----------|------|-------------|
| `agents/foo.agent.md` | Agent | Does X for Y |
| `instructions/foo.instructions.md` | Instruction | Also does X for Y |

**Why flagged:** <Brief explanation of the similarity>

---

#### Group 2: ...

<repeat for each group>
```

Use blocos `<details>` para agrupar os itens se houver mais de 10.

### Orientações para uma saída segura

- Se você encontrar possíveis duplicatas: use `create-__PRESERVE_0__` para enviar o relatório.
- Se **nenhuma** possível duplicata for encontrada (após excluir as duplicatas conhecidas e aceitas): chame `noop` com a mensagem: "Nenhum recurso potencialmente duplicado foi detectado. Todos os recursos parecem ter finalidades distintas."

## Diretrizes

- Seja cauteloso — sinalize recursos apenas quando houver um risco real de redundância.
- Agrupe as duplicatas relacionadas (não liste o mesmo par duas vezes em grupos diferentes).
- Classifique os grupos por nível de confiança (começando pelos sinais duplicados mais fortes).
- Incluir duplicatas de tipo cruzado (por exemplo, um agente e uma instrução que realizam a mesma ação).
- Limite o relatório aos 20 principais grupos com maior probabilidade de duplicidade para que ele seja prático.
- Para as habilidades, use o nome da pasta e a descrição de `__PRESERVE_0__`.
- Processe os recursos em lotes para cumprir os prazos — priorize a comparação de nomes e descrições e, em seguida, verifique aleatoriamente o conteúdo dos principais candidatos.
