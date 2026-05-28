---
description: 'Realize tarefas de manutenção em código C#/.NET incluindo limpeza, modernização e remediação de débito técnico.'
name: 'Atualização .NET'
tools: ['codebase', 'edit/editFiles', 'search', 'runCommands', 'runTasks', 'runTests', 'problems', 'changes', 'usages', 'findTestFiles', 'testFailure', 'terminalLastCommand', 'terminalSelection', 'web/fetch', 'microsoft.docs.mcp']
---

# Coleção de Atualização .NET

Especialista em atualização do .NET Framework para migração abrangente de projetos

**Tags:** dotnet, upgrade, migration, framework, modernization

## Uso da Coleção

### Modo Chat de Atualização .NET

Descubra e planeje sua jornada de atualização .NET!

```markdown, upgrade-analysis.prompt.md
---
mode: dotnet-upgrade
title: Analisar versões atuais do .NET framework e criar plano de atualização
---
Analise o repositório e liste o TargetFramework atual de cada projeto
juntamente com a versão LTS mais recente disponível no cronograma de lançamento da Microsoft.
Crie uma estratégia de atualização priorizando projetos menos dependentes primeiro.
```

O modo chat de atualização se adapta automaticamente à versão atual do .NET no seu repositório e fornece orientação contextual de atualização para a próxima versão estável.

Ele ajudará você a:
- Detectar automaticamente versões atuais do .NET em todos os projetos
- Gerar sequências de atualização otimizadas
- Identificar mudanças incompatíveis e oportunidades de modernização
- Criar fluxos de atualização por projeto

---

### Instruções de Atualização .NET

Execute atualizações abrangentes do .NET framework com orientação estruturada!

As instruções fornecem:
- Estratégias de atualização sequencial
- Análise e sequenciamento de dependências
- Direcionamento de framework e ajustes de código
- Gerenciamento de NuGet e dependências
- Atualizações de pipeline CI/CD
- Procedimentos de teste e validação

Use essas instruções ao implementar planos de atualização para garantir execução e validação adequadas.

---

### Prompts de Atualização .NET

Acesso rápido a prompts de análise de atualização especializados!

A coleção de prompts inclui consultas prontas para uso para:
- Descoberta e avaliação de projetos
- Estratégia de atualização e sequenciamento
- Direcionamento de framework e ajustes de código
- Análise de mudanças incompatíveis
- Atualizações de pipeline CI/CD
- Validação final e entrega

Use esses prompts para análise direcionada de aspectos específicos da atualização.

---

## Início Rápido
1. Execute uma passagem de descoberta para enumerar todos os arquivos `*.sln` e `*.csproj` no repositório.
2. Detecte a(s) versão(ões) atual(is) do .NET usada(s) nos projetos.
3. Identifique a versão estável mais recente disponível do .NET (LTS preferível) — geralmente `+2` anos à frente da versão existente.
4. Gere um plano de atualização para mover da versão atual → próxima versão estável (ex.: `net6.0 → net8.0`, ou `net7.0 → net9.0`).
5. Atualize um projeto por vez, valide builds, atualize testes e modifique CI/CD adequadamente.

---

## Detectar Automaticamente a Versão Atual do .NET
Para detectar automaticamente as versões de framework na solução:

```bash
# 1. Verificar SDKs globais instalados
dotnet --list-sdks

# 2. Detectar TargetFrameworks no nível do projeto
find . -name "*.csproj" -exec grep -H "<TargetFramework" {} \;

# 3. Opcional: resumir versões únicas de framework
grep -r "<TargetFramework" **/*.csproj | sed 's/.*<TargetFramework>//;s/<\/TargetFramework>//' | sort | uniq

# 4. Verificar ambiente de runtime
dotnet --info | grep "Version"
```

**Prompt de Chat:**
> "Analise o repositório e liste o TargetFramework atual de cada projeto juntamente com a versão LTS mais recente disponível no cronograma de lançamento da Microsoft."

---

## Comandos de Descoberta e Análise
```bash
# Listar todos os projetos
dotnet sln list

# Verificar frameworks de destino atuais para cada projeto
grep -H "TargetFramework" **/*.csproj

# Verificar pacotes desatualizados
dotnet list <ProjectName>.csproj package --outdated

# Gerar grafo de dependências
dotnet msbuild <ProjectName>.csproj /t:GenerateRestoreGraphFile /p:RestoreGraphOutputPath=graph.json
```

**Prompt de Chat:**
> "Analise a solução e resuma o TargetFramework atual de cada projeto e sugira a próxima versão LTS de atualização apropriada."

---

## Regras de Classificação
- `TargetFramework` começa com `netcoreapp`, `net5.0+`, `net6.0+`, etc. → **.NET Moderno**
- `netstandard*` → **.NET Standard** (migrar para versão atual do .NET)
- `net4*` → **.NET Framework** (migrar via etapa intermediária para .NET 8+)

---

## Sequência de Atualização
1. **Comece com Bibliotecas Independentes:** Bibliotecas de classes menos dependentes primeiro.
2. **Próximo:** Componentes compartilhados e utilitários comuns.
3. **Depois:** Projetos de API, Web ou Function.
4. **Finalmente:** Testes, pontos de integração e pipelines.

**Prompt de Chat:**
> "Gere a ordem de atualização ideal para este repositório, priorizando projetos menos dependentes primeiro."

---

## Fluxo de Atualização por Projeto
1. **Criar branch:** `upgrade/<project>-to-<targetVersion>`
2. **Editar `<TargetFramework>`** no `.csproj` para a versão sugerida (ex.: `net9.0`)
3. **Restaurar e atualizar pacotes:**
   ```bash
   dotnet restore
   dotnet list package --outdated
   dotnet add package <PackageName> --version <LatestVersion>
   ```
4. **Build e teste:**
   ```bash
   dotnet build <ProjectName>.csproj
   dotnet test <ProjectName>.Tests.csproj
   ```
5. **Corrigir problemas** — resolver APIs descontinuadas, ajustar configurações, modernizar JSON/logging/DI.
6. **Commit e push** PR com evidência de testes e checklist.

---

## Mudanças Incompatíveis e Modernização
- Use o `.NET Upgrade Assistant` para recomendações iniciais.
- Aplique analyzers para detectar APIs obsoletas.
- Substitua SDKs desatualizados (ex.: `Microsoft.Azure.*` → `Azure.*`).
- Modernize lógica de inicialização (`Startup.cs` → `Program.cs` top-level statements).

**Prompt de Chat:**
> "Liste APIs descontinuadas ou incompatíveis ao atualizar de <currentVersion> para <targetVersion> para <ProjectName>."

---

## Atualizações de Configuração CI/CD
Garanta que os pipelines usem a **versão de destino** detectada dinamicamente:

**Azure DevOps**
```yaml
- task: UseDotNet@2
  inputs:
    packageType: 'sdk'
    version: '$(TargetDotNetVersion).x'
```

**GitHub Actions**
```yaml
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '${{ env.TargetDotNetVersion }}.x'
```

---

## Checklist de Validação
- [ ] TargetFramework atualizado para próxima versão estável
- [ ] Todos os pacotes NuGet compatíveis e atualizados
- [ ] Pipelines de build e teste bem-sucedidos localmente e em CI
- [ ] Testes de integração passam
- [ ] Implantado em ambiente inferior e verificado

---

## Estratégia de Branching e Rollback
- Use feature branches: `upgrade/<project>-to-<targetVersion>`
- Faça commits frequentes e mantenha mudanças atômicas
- Se CI falhar após merge, reverta PR e isole módulos com falha

**Prompt de Chat:**
> "Sugira um plano de rollback e validação se a atualização .NET para <ProjectName> introduzir regressões de build ou runtime."

---

## Automação e Escalabilidade
- Automatize detecção de atualização com GitHub Actions ou Azure Pipelines.
- Agende execuções noturnas para verificar novos lançamentos .NET via `dotnet --list-sdks`.
- Use agentes para automaticamente criar PRs para frameworks desatualizados.

---

## Biblioteca de Prompts do Chatmode
1. "Liste todos os projetos com versões .NET atuais e recomendadas."
2. "Gere um plano de atualização por projeto de <currentVersion> para <targetVersion>."
3. "Sugira edições de .csproj e pipeline para atualizar <ProjectName>."
4. "Resuma resultados de build/teste pós-atualização para <ProjectName>."
5. "Crie descrição de PR e checklist para a atualização."

---
