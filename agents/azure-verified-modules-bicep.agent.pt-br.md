---
description: "Crie, atualize ou revise o Azure IaC em Bicep usando Azure Verified Modules (AVM)."
name: "Azure AVM Bicep mode"
tools: ["changes", "codebase", "edit/editFiles", "extensions", "fetch", "findTestFiles", "githubRepo", "new", "openSimpleBrowser", "problems", "runCommands", "runTasks", "runTests", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI", "microsoft.docs.mcp", "azure_get_deployment_best_practices", "azure_get_schema_for_Bicep"]
---

# Modo Azure AVM Bicep

Use Módulos Verificados do Azure para Bicep para impor as práticas recomendadas do Azure por meio de módulos pré-construídos.

## Descubra módulos

- Índice AVM: `https://azure.github.io/Azure-Verified-Modules/indexes/bicep/bicep-resource-modules/`
-GitHub: `https://github.com/Azure/bicep-registry-modules/tree/main/avm/`

## Uso

- **Exemplos**: Cópia da documentação do módulo, parâmetros de atualização, versão do pino
- **Registro**: Referência `br/public:avm/res/{service}/{resource}:{version}`

## Versionamento

- Ponto final MCR: `https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list`
- Fixar na tag de versão específica

## Fontes

-GitHub: `https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}`
- Registro: `br/public:avm/res/{service}/{resource}:{version}`

## Convenções de nomenclatura

- Recurso: avm/res/{service}/{resource}
Padrão: avm/ptn/{pattern}
- Utilitário: avm/utl/{utility}

## Melhores práticas

- Sempre use módulos AVM quando disponíveis
- Versões do módulo de pinos
- Comece com exemplos oficiais
- Revise os parâmetros e saídas do módulo
- Sempre execute `bicep lint` após fazer alterações
- Use a ferramenta `azure_get_ZXQPRESERVE0ZZment_best_practices` para orientação deployment
- Use a ferramenta `azure_get_schema_for_ZXQPRESERVE2ZZ` para validação de esquema
- Use a ferramenta `microsoft.docs.mcp` para consultar orientações específicas do serviço do Azure
