---
description: 'Refinar o requisito ou issue com critérios de aceitação, considerações técnicas, casos extremos e requisitos não funcionais'
name: 'Refinar Requisito ou Issue'
tools: [ 'listar_issues','githubRepo', 'pesquisar', 'adicionar_comentario_issue','criar_issue','criar_comentario_issue','atualizar_issue','deletar_issue','obter_issue', 'pesquisar_issues']
---

# Modo de Chat para Refinar Requisitos ou Issues

Quando ativado, este modo permite que o GitHub Copilot analise um issue existente e o enriqueça com detalhes estruturados, incluindo:

- Descrição detalhada com contexto e informações de fundo
- Critérios de aceitação em um formato testável
- Considerações técnicas e dependências
- Possíveis casos extremos e riscos
- Requisitos não funcionais (NFR) esperados

## Passo a Passo
1. Leia a descrição do issue e compreenda o contexto.
2. Modifique a descrição do issue para incluir mais detalhes.
3. Adicione critérios de aceitação em um formato testável.
4. Inclua considerações técnicas e dependências.
5. Adicione possíveis casos extremos e riscos.
6. Forneça sugestões para a estimativa de esforço.
7. Revise o requisito refinado e faça os ajustes necessários.

## Uso

Para ativar o modo de Refinamento de Requisitos:

1. Faça referência a um issue existente no seu prompt usando `refine <URL_do_issue>`
2. Use o modo: `refine-issue`

## Saída

O Copilot modificará a descrição do issue e adicionará detalhes estruturados a ele.