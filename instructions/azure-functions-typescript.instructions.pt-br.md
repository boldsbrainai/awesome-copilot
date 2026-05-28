---
description: 'Padrões TypeScript para Azure Functions'
applyTo: '**/*.ts, **/*.js, **/*.json'
---

## Orientações para a geração de código
- Gerar código TypeScript moderno para Node.js
- Utilize `async/await` para código assíncrono
- Sempre que possível, utilize os módulos integrados do Node.js v20 em vez de pacotes externos
- Sempre utilize funções assíncronas do tipo Node.js, como `node:fs/promises` em vez de `fs`, para evitar bloquear o ciclo de eventos
- Consulte antes de adicionar quaisquer dependências extras ao projeto
- A API foi desenvolvida com o Azure Functions utilizando o pacote `@azure/functions@4`.
- Cada endpoint deve ter seu próprio arquivo de função, e seguir a seguinte convenção de nomenclatura: `src/functions/<nome-do-recurso>-<http-verb>.ts`
- Ao fazer alterações na API, certifique-se de atualizar o esquema OpenAPI (se existir) e o arquivo `README.md` de acordo.