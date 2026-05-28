---
description: 'Arquivos CFM do ColdFusion e padrões de aplicativos'
applyTo: "**/*.cfm"
---

# Padrões de codificação do ColdFusion

- Sempre que possível, use CFScript para obter uma sintaxe mais clara.
- Evite usar tags e funções obsoletas.
- Siga convenções de nomenclatura consistentes para variáveis e componentes.
- Use `cfqueryparam` para evitar injeção de SQL.
- Escape os símbolos de hash CSS dentro de blocos `<cfoutput>` usando `##`.
- Ao usar HTMX dentro de blocos `<cfoutput>`, escape os símbolos de cerquilha (`#`) utilizando duas cerquilhas (`##`) para evitar a interpolação indesejada de variáveis.
- Se você estiver em um arquivo de destino HTMX, certifique-se de que a primeira linha seja: `<cfsetting showDebugOutput = "false">`

# Boas práticas adicionais

- Use `Application.cfc` para configurações do aplicativo e tratamento de solicitações.
- Organize o código em CFCs (componentes) reutilizáveis para facilitar a manutenção.
- Valide e limpe todas as entradas do usuário.
- Use `cftry`/`cfcatch` para o tratamento de erros e o registro em log.
- Evite inserir credenciais ou dados confidenciais diretamente nos arquivos-fonte.
- Use recuo consistente (2 espaços, de acordo com os padrões globais).
- Comente a lógica complexa e documente funções com descrições e parâmetros.
- Dê preferência a `cfinclude` para modelos compartilhados, mas evite inclusões circulares.

- Use operadores ternários sempre que possível
- Certifique-se de que o alinhamento das tabulações seja consistente.