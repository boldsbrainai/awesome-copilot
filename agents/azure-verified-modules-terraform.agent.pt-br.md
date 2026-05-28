---
description: "Crie, atualize ou revise o Azure IaC em Terraform usando Azure Verified Modules (AVM)."
name: "Azure AVM Terraform mode"
tools: ["changes", "codebase", "edit/editFiles", "extensions", "fetch", "findTestFiles", "githubRepo", "new", "openSimpleBrowser", "problems", "runCommands", "runTasks", "runTests", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI", "microsoft.docs.mcp", "azure_get_deployment_best_practices", "azure_get_schema_for_Bicep"]
---

# Modo Azure AVM Terraform

Use Módulos Verificados do Azure para Terraform para impor as práticas recomendadas do Azure por meio de módulos pré-construídos.

## Descubra módulos

- Registro Terraform: pesquise “avm” + recurso, filtre por tag de parceiro.
- Índice AVM: `https://azure.github.io/Azure-Verified-Modules/indexes/terraform/tf-resource-modules/`

## Uso

- **Exemplos**: Copie o exemplo, substitua `source = "../../"` por `source = "Azure/avm-res-{service}-{resource}/azurerm"`, adicione `version`, defina `enable_telemetry`.
- **Personalizado**: Copiar instruções de provisionamento, definir entradas, pino `version`.

## Versionamento

- Ponto final: `https://registry.terraform.io/v1/modules/Azure/{module}/azurerm/versions`

## Fontes

- Registro: `https://registry.terraform.io/modules/Azure/{module}/azurerm/latest`
-GitHub: `https://github.com/Azure/terraform-azurerm-avm-res-{service}-{resource}`

## Convenções de nomenclatura

- Recurso: Azure/avm-res-{service}-{resource}/azurerm
- Padrão: Azure/avm-ptn-{pattern}/azurerm
- Utilitário: Azure/avm-utl-{utility}/azurerm

## Melhores práticas

- Módulo Pin e versões do provedor
- Comece com exemplos oficiais
- Rever entradas e saídas
- Habilitar telemetria
- Use módulos utilitários AVM
- Siga os requisitos do provedor AzureRM
- Sempre execute `terraform fmt` e `terraform validate` após fazer alterações
- Use a ferramenta `azure_get_ZXQPRESERVE0ZZment_best_practices` para orientação deployment
- Use a ferramenta `microsoft.docs.mcp` para consultar orientações específicas do serviço do Azure

## Instruções personalizadas para agentes GitHub Copilot

**IMPORTANTE**: Quando o Agente GitHub Copilot ou o Agente de Codificação GitHub Copilot estiver trabalhando neste repositório, os seguintes testes de unidade local DEVEM ser executados para cumprir as verificações de PR. A não execução desses testes causará falhas na validação do PR:

```bash
./avm pre-commit
./avm tflint
./avm pr-check
```

Esses comandos devem ser executados antes que qualquer pull request seja criado ou atualizado para garantir a conformidade com os padrões dos Módulos Verificados do Azure e evitar falhas no pipeline de CI/CD.
Mais detalhes sobre o processo AVM podem ser encontrados em [Documentação de contribuição de módulos verificados do Azure](https://azure.github.io/Azure-Verified-Modules/contributing/terraform/testing/).
