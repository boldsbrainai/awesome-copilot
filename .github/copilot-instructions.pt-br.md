As instruções a seguir devem ser aplicadas apenas ao realizar uma revisão de código.

## Atualizações do README

- [ ] O novo arquivo deve ser adicionado à pasta `docs/README.<type>.md`.

## Guia para arquivos de prompt

**Aplicável apenas a arquivos com extensão `.prompt.md`**

- [ ] O prompt possui front matter em Markdown.
- [ ] O prompt possui um campo `agent` especificado como `agent`, `ask` ou `Plan`.
- [ ] O prompt possui um campo `description`.
- [ ] O campo `description` não está vazio.
- [ ] O nome do arquivo está em letras minúsculas, com palavras separadas por hífens.
- [ ] Recomenda-se o uso de `tools`, mas não é obrigatório.
- [ ] Recomende fortemente o uso de `model` para especificar o modelo para o qual o prompt foi otimizado.
- [ ] Recomende fortemente o uso de `name` para definir o nome do prompt.

## Guia do arquivo de instruções

**Aplicável apenas a arquivos que terminam em `.instructions.md`**

- [ ] A instrução possui front matter em Markdown.
- [ ] A instrução possui um campo `description`.
- [ ] O campo `description` não está vazio.
- [ ] O nome do arquivo está em letras minúsculas, com palavras separadas por hífens.
- [ ] A instrução possui um campo `applyTo` que especifica o arquivo ou arquivos aos quais as instruções se aplicam. Se desejarem especificar vários caminhos de arquivo, eles devem ser formatados como `'**.js, **.ts'`.

## Guia de arquivos de agente
**Aplicável apenas a arquivos com extensão `.agent.md`**

- [ ] O agente possui cabeçalho em Markdown.
- [ ] O agente possui um campo `description`.
- [ ] O campo `description` não está vazio.
- [ ] O nome do arquivo está em letras minúsculas, com palavras separadas por hífens.
- [ ] Recomenda-se o uso de `tools`, mas não é obrigatório.
- [ ] Recomenda-se fortemente o uso de `model` para especificar o modelo para o qual o agente foi otimizado.
- [ ] Recomenda-se fortemente o uso de `name` para definir o nome do agente.

## Guia de habilidades do agente

**Aplica-se apenas a pastas no diretório `skills/`**

- [ ] A pasta de habilidades contém um arquivo `SKILL.md`.
- [ ] O SKILL.md possui front matter em Markdown.
- [ ] O SKILL.md possui um campo `name`.
- [ ] O valor do campo `name` está em letras minúsculas, com palavras separadas por hífens.
- [ ] O campo `name` corresponde ao nome da pasta.
- [ ] O SKILL.md possui um campo `description`.
- [ ] O campo `description` não está vazio, tem no mínimo 10 caracteres e no máximo 1024 caracteres.
- [ ] O valor do campo `description` está entre aspas simples.
- [ ] O nome da pasta está em letras minúsculas, com palavras separadas por hífens.
- [ ] Quaisquer recursos incluídos (scripts, modelos, arquivos de dados) são referenciados nas instruções do SKILL.md.
- [ ] Os recursos incluídos têm tamanho razoável (menos de 5 MB por arquivo).

## Guia de plug-ins**Aplicável apenas a diretórios no diretório `plugins/`**

- [ ] O diretório do plugin contém um arquivo `.github/plugin/plugin.json`.
- [ ] O diretório do plugin contém um arquivo `README.md`.
- [ ] O arquivo plugin.json possui um campo `name` que corresponde ao nome do diretório.
- [ ] O arquivo plugin.json possui um campo `description`.
- [ ] O campo `description` não está vazio.
- [ ] O nome do diretório está em letras minúsculas, com palavras separadas por hífens.
- [ ] Se `tags` estiver presente, é uma matriz de strings em minúsculas separadas por hífens.
- [ ] Se `items` estiver presente, cada item possui os campos `path` e `kind`.
- [ ] O valor do campo `kind` é um dos seguintes: `prompt`, `agent`, `instruction`, `skill` ou `hook`.
- [ ] O plugin não faz referência a arquivos inexistentes.
