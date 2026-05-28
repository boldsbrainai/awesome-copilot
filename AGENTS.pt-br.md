# AGENTS.md

## Visão Geral do Projeto

O repositório Awesome GitHub Copilot é uma coleção orientada pela comunidade de agentes e instruções personalizados projetados para aprimorar as experiências com GitHub Copilot em vários domínios, linguagens e casos de uso. O projeto inclui:

- **Agents** - Agentes especializados do GitHub Copilot que se integram a servidores MCP
- **Instructions** - Padrões de código e boas práticas aplicados a padrões específicos de arquivos
- **Skills** - Pastas autônomas com instruções e recursos empacotados para tarefas especializadas
- **Hooks** - Fluxos de trabalho automatizados acionados por eventos específicos durante o desenvolvimento
- **Workflows** - [Agentic Workflows](https://github.github.com/gh-aw) para automação de repositório com IA no GitHub Actions
- **Plugins** - Pacotes instaláveis que agrupam agentes, comandos e skills relacionados em torno de temas específicos

## Estrutura do Repositório

```text
.
├── agents/           # Definições personalizadas de agentes do GitHub Copilot (arquivos .agent.md)
├── instructions/     # Padrões de código e diretrizes (arquivos .instructions.md)
├── skills/           # Pastas de Agent Skills (cada uma com SKILL.md e recursos empacotados opcionais)
├── hooks/            # Hooks de fluxos de trabalho automatizados (pastas com README.md + hooks.json)
├── workflows/        # Agentic Workflows (arquivos .md para automação no GitHub Actions)
├── plugins/          # Pacotes de plugin instaláveis (pastas com plugin.json)
├── docs/             # Documentação para diferentes tipos de recurso
├── eng/              # Scripts de build e automação
└── scripts/          # Scripts utilitários
```

## Comandos de Configuração

```bash
# Instalar dependências
npm ci

# Compilar o projeto (gera README.md e marketplace.json)
npm run build

# Validar manifestos de plugin
npm run plugin:validate

# Gerar apenas marketplace.json
npm run plugin:generate-marketplace

# Criar um novo plugin
npm run plugin:create -- --name <plugin-name>

# Validar skills de agentes
npm run skill:validate

# Criar uma nova skill
npm run skill:create -- --name <skill-name>
```

## Fluxo de Desenvolvimento

### Trabalhando com Agents, Instructions, Skills e Hooks

Todos os arquivos de agente (`*.agent.md`) e de instrução (`*.instructions.md`) devem incluir um front matter Markdown adequado. Agent Skills são pastas que contêm um arquivo `SKILL.md` com front matter e recursos empacotados opcionais. Hooks são pastas que contêm um `README.md` com front matter e um arquivo de configuração `hooks.json`:

#### Arquivos de Agente (*.agent.md)
- Devem ter o campo `description` (envolto em aspas simples)
- Os nomes de arquivo devem estar em minúsculas, com palavras separadas por hífens
- Recomenda-se incluir o campo `tools`
- Recomenda-se fortemente especificar o campo `model`

#### Arquivos de Instrução (*.instructions.md)
- Devem ter o campo `description` (envolto em aspas simples, não vazio)
- Devem ter o campo `applyTo` especificando padrões de arquivo (por exemplo, `'**.js, **.ts'`)
- Os nomes de arquivo devem estar em minúsculas, com palavras separadas por hífens

#### Agent Skills (skills/*/SKILL.md)
- Cada skill é uma pasta que contém um arquivo `SKILL.md`
- O SKILL.md deve ter o campo `name` (em minúsculas com hífens, correspondendo ao nome da pasta, máximo de 64 caracteres)
- O SKILL.md deve ter o campo `description` (envolto em aspas simples, de 10 a 1024 caracteres)
- Os nomes de pasta devem estar em minúsculas, com palavras separadas por hífens
- Skills podem incluir recursos empacotados (scripts, templates, arquivos de dados)
- Os recursos empacotados devem ser referenciados nas instruções do SKILL.md
- Os arquivos de recurso devem ter tamanho razoável (menos de 5MB por arquivo)
- Skills seguem a [especificação Agent Skills](https://agentskills.io/specification)

#### Pastas de Hook (hooks/*/README.md)
- Cada hook é uma pasta que contém um arquivo `README.md` com front matter
- O README.md deve ter o campo `name` (nome legível por humanos)
- O README.md deve ter o campo `description` (envolto em aspas simples, não vazio)
- Deve incluir um arquivo `hooks.json` com a configuração do hook (eventos de hook extraídos desse arquivo)
- Os nomes de pasta devem estar em minúsculas, com palavras separadas por hífens
- Podem incluir recursos empacotados (scripts, utilitários, arquivos de configuração)
- Scripts empacotados devem ser referenciados no README.md e no hooks.json
- Siga a [especificação de hooks do GitHub Copilot](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/use-hooks)
- Opcionalmente inclui o campo `tags` para categorização

#### Arquivos de Workflow (workflows/*.md)
- Cada workflow é um arquivo `.md` independente no diretório `workflows/`
- Deve ter o campo `name` (nome legível por humanos)
- Deve ter o campo `description` (envolto em aspas simples, não vazio)
- Contém front matter de workflow agentic (`on`, `permissions`, `safe-outputs`) e instruções em linguagem natural
- Os nomes de arquivo devem estar em minúsculas, com palavras separadas por hífens
- Apenas arquivos `.md` são aceitos — arquivos `.yml`, `.yaml` e `.lock.yml` são bloqueados pela CI
- Siga a [especificação GitHub Agentic Workflows](https://github.github.com/gh-aw/reference/workflow-structure/)

#### Pastas de Plugin (plugins/*)
- Cada plugin é uma pasta que contém um arquivo `.github/plugin/plugin.json` com metadados
- O plugin.json deve ter o campo `name` (correspondendo ao nome da pasta)
- O plugin.json deve ter o campo `description` (descrevendo a finalidade do plugin)
- O plugin.json deve ter o campo `version` (versão semântica, por exemplo, "1.0.0")
- O conteúdo do plugin é definido declarativamente em plugin.json usando campos da especificação Claude Code (`agents`, `commands`, `skills`). Os arquivos-fonte ficam em diretórios de nível superior e são materializados em plugins pela CI.
- O arquivo `marketplace.json` é gerado automaticamente a partir de todos os plugins durante o build
- Plugins podem ser descobertos e instalados via GitHub Copilot CLI

### Adicionando Novos Recursos

Ao adicionar um novo agente, instrução, skill, hook, workflow ou plugin:

**Para Agents e Instructions:**
1. Crie o arquivo com o front matter adequado
2. Adicione o arquivo ao diretório apropriado
3. Atualize o README.md executando: `npm run build`
4. Verifique se o recurso aparece no README gerado

**Para Hooks:**
1. Crie uma nova pasta em `hooks/` com um nome descritivo
2. Crie `README.md` com front matter adequado (name, description, hooks, tags)
3. Crie `hooks.json` com a configuração do hook seguindo a especificação de hooks do GitHub Copilot
4. Adicione à pasta quaisquer scripts ou recursos empacotados
5. Torne os scripts executáveis: `chmod +x script.sh`
6. Atualize o README.md executando: `npm run build`
7. Verifique se o hook aparece no README gerado


**Para Workflows:**
1. Crie um novo arquivo `.md` em `workflows/` com um nome descritivo (por exemplo, `daily-issues-report.md`)
2. Inclua front matter com `name` e `description`, além dos campos de workflow agentic (`on`, `permissions`, `safe-outputs`)
3. Compile com `gh aw compile --validate` para verificar se é válido
4. Atualize o README.md executando: `npm run build`
5. Verifique se o workflow aparece no README gerado


**Para Skills:**
1. Execute `npm run skill:create` para criar o esqueleto de uma nova pasta de skill
2. Edite o arquivo SKILL.md gerado com suas instruções
3. Adicione quaisquer recursos empacotados (scripts, templates, dados) à pasta da skill
4. Execute `npm run skill:validate` para validar a estrutura da skill
5. Atualize o README.md executando: `npm run build`
6. Verifique se a skill aparece no README gerado

**Para Plugins:**
1. Execute `npm run plugin:create -- --name <plugin-name>` para criar o esqueleto de um novo plugin
2. Defina agentes, comandos e skills em `plugin.json` usando campos da especificação Claude Code
3. Edite o `plugin.json` gerado com seus metadados
4. Execute `npm run plugin:validate` para validar a estrutura do plugin
5. Execute `npm run build` para atualizar README.md e marketplace.json
6. Verifique se o plugin aparece em `.github/plugin/marketplace.json`

**Para Plugins Externos:**
1. Edite `plugins/external.json` e adicione uma entrada com `name`, `source`, `description` e `version`
2. O campo `source` deve ser um objeto que especifique um repositório GitHub, uma URL git, um pacote npm ou um pacote pip (consulte [CONTRIBUTING.md](CONTRIBUTING.md#adding-external-plugins))
3. Execute `npm run build` para regenerar marketplace.json
4. Verifique se o plugin externo aparece em `.github/plugin/marketplace.json`

### Instruções de Teste

```bash
# Executar todas as verificações de validação
npm run plugin:validate
npm run skill:validate

# Compilar e verificar a geração do README
npm run build

# Corrigir finais de linha (obrigatório antes de fazer commit)
bash scripts/fix-line-endings.sh
```

Antes de fazer commit:
- Certifique-se de que todo o front matter Markdown esteja formatado corretamente
- Verifique se os nomes de arquivo seguem a convenção de minúsculas com hífens
- Execute `npm run build` para atualizar o README
- **Sempre execute `bash scripts/fix-line-endings.sh`** para normalizar os finais de linha (CRLF → LF)
- Confira se seu novo recurso aparece corretamente no README

## Diretrizes de Estilo de Código

### Arquivos Markdown
- Use front matter adequado com os campos obrigatórios
- Mantenha as descrições concisas e informativas
- Envolva os valores do campo `description` em aspas simples
- Use nomes de arquivo em minúsculas com hífens como separadores

### Scripts JavaScript/Node.js
- Localizados nos diretórios `eng/` e `scripts/`
- Siga as convenções de módulo ES do Node.js (extensão `.mjs`)
- Use nomes claros e descritivos para funções e variáveis

## Diretrizes para Pull Request

Ao criar uma pull request:

> **Importante:** Todas as pull requests devem ter como destino a branch **`staged`**, não `main`.

1. **Atualizações de README**: Novos arquivos devem ser adicionados automaticamente ao README quando você executar `npm run build`
2. **Validação de front matter**: Certifique-se de que todos os arquivos Markdown tenham os campos obrigatórios de front matter
3. **Nomeação de arquivos**: Verifique se todos os novos arquivos seguem a convenção de minúsculas com hífens
4. **Verificação de build**: Execute `npm run build` antes de fazer commit para verificar a geração do README
5. **Finais de linha**: **Sempre execute `bash scripts/fix-line-endings.sh`** para normalizar os finais de linha para LF (estilo Unix)
6. **Descrição**: Forneça uma descrição clara do que seu agente/instrução faz
7. **Teste**: Se estiver adicionando um plugin, execute `npm run plugin:validate` para garantir a validade

### Checklist Pré-commit

Antes de enviar sua PR, certifique-se de que você:
- [ ] Executou `npm install` (ou `npm ci`) para instalar dependências
- [ ] Executou `npm run build` para gerar o README.md atualizado
- [ ] Executou `bash scripts/fix-line-endings.sh` para normalizar os finais de linha
- [ ] Verificou que todos os novos arquivos têm front matter adequado
- [ ] Testou que sua contribuição funciona com GitHub Copilot
- [ ] Conferiu que os nomes de arquivo seguem a convenção de nomenclatura

### Checklist de Code Review

Para arquivos de instrução (*.instructions.md):
- [ ] Tem front matter Markdown
- [ ] Tem campo `description` não vazio envolto em aspas simples
- [ ] Tem campo `applyTo` com padrões de arquivo
- [ ] O nome do arquivo está em minúsculas com hífens

Para arquivos de agente (*.agent.md):
- [ ] Tem front matter Markdown
- [ ] Tem campo `description` não vazio envolto em aspas simples
- [ ] Tem campo `name` com nome legível por humanos (por exemplo, "Resolver Comentários" e não "address-comments")
- [ ] O nome do arquivo está em minúsculas com hífens
- [ ] Inclui o campo `model` (fortemente recomendado)
- [ ] Considera usar o campo `tools`

Para skills (skills/*/):
- [ ] A pasta contém um arquivo SKILL.md
- [ ] O SKILL.md tem front matter Markdown
- [ ] Tem o campo `name` correspondendo ao nome da pasta (em minúsculas com hífens, máximo de 64 caracteres)
- [ ] Tem campo `description` não vazio envolto em aspas simples (10-1024 caracteres)
- [ ] O nome da pasta está em minúsculas com hífens
- [ ] Quaisquer recursos empacotados são referenciados no SKILL.md
- [ ] Os recursos empacotados têm menos de 5MB por arquivo

Para pastas de hook (hooks/*/):
- [ ] A pasta contém um arquivo README.md com front matter Markdown
- [ ] Tem campo `name` com nome legível por humanos
- [ ] Tem campo `description` não vazio envolto em aspas simples
- [ ] Tem arquivo `hooks.json` com configuração de hook válida (eventos de hook extraídos desse arquivo)
- [ ] O nome da pasta está em minúsculas com hífens
- [ ] Quaisquer scripts empacotados são executáveis e referenciados no README.md
- [ ] Segue a [especificação de hooks do GitHub Copilot](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/use-hooks)
- [ ] Opcionalmente inclui o campo de array `tags` para categorização

Para arquivos de workflow (workflows/*.md):
- [ ] O arquivo tem front matter Markdown
- [ ] Tem campo `name` com nome legível por humanos
- [ ] Tem campo `description` não vazio envolto em aspas simples
- [ ] O nome do arquivo está em minúsculas com hífens
- [ ] Contém `on` e `permissions` no front matter
- [ ] O workflow usa permissões de privilégio mínimo e saídas seguras
- [ ] Nenhum arquivo `.yml`, `.yaml` ou `.lock.yml` incluído
- [ ] Segue a [especificação GitHub Agentic Workflows](https://github.github.com/gh-aw/reference/workflow-structure/)

Para plugins (plugins/*/):
- [ ] O diretório contém um arquivo `.github/plugin/plugin.json`
- [ ] O diretório contém um arquivo `README.md`
- [ ] O `plugin.json` tem campo `name` correspondendo ao nome do diretório (em minúsculas com hífens)
- [ ] O `plugin.json` tem campo `description` não vazio
- [ ] O `plugin.json` tem campo `version` (versão semântica, por exemplo, "1.0.0")
- [ ] O nome do diretório está em minúsculas com hífens
- [ ] Se `keywords` estiver presente, é um array de strings em minúsculas separadas por hífens
- [ ] Se os arrays `agents`, `commands` ou `skills` estiverem presentes, cada entrada é um caminho relativo válido
- [ ] O plugin não referencia arquivos inexistentes
- [ ] Execute `npm run build` para verificar se marketplace.json é atualizado corretamente

## Contribuindo

Este é um projeto orientado pela comunidade. Contribuições são bem-vindas! Consulte:
- [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes de contribuição
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) para padrões da comunidade
- [SECURITY.md](SECURITY.md) para políticas de segurança

## Servidor MCP

O repositório inclui um Servidor MCP (Model Context Protocol) para pesquisar e instalar recursos diretamente deste repositório. Docker é necessário para executar o servidor.

## Licença

Licença MIT - consulte [LICENSE](LICENSE) para detalhes
