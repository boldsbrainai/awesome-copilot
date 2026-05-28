# Napkin — Quadro Branco Visual para o Copilot CLI

Um quadro branco que abre no seu navegador e se conecta ao Copilot CLI. Desenhe, faça esboços, adicione notas adesivas — depois compartilhe tudo de volta com o Copilot. O Copilot vê seus desenhos e responde com análises, sugestões e ideias.

Criado para pessoas que não são desenvolvedoras de software: advogados, PMs, stakeholders de negócio, designers, redatores — qualquer pessoa que pense melhor de forma visual.

## Instalação

Instale o plugin diretamente pelo Copilot CLI:

```bash
copilot plugin install napkin@awesome-copilot
```

É só isso. Nenhum outro software, conta ou configuração é necessário.

### Verifique se está instalado

Execute isto no Copilot CLI para confirmar que o plugin está disponível:

```
/skills
```

Você deverá ver **napkin** na lista de skills disponíveis.

## Como usar

### Passo 1: Diga "let's napkin"

Abra o Copilot CLI e digite `let's napkin` (ou "open a napkin" ou "start a whiteboard"). O Copilot cria um quadro branco e o abre no seu navegador.

![Passo 1 — Ative o napkin](../../skills/napkin/assets/step1-activate.svg)

### Passo 2: Seu quadro branco abre

Um quadro branco limpo aparece no seu navegador com ferramentas simples de desenho. Se for sua primeira vez, uma mensagem rápida de boas-vindas explica como tudo funciona.

![Passo 2 — O quadro branco abre](../../skills/napkin/assets/step2-whiteboard.svg)

### Passo 3: Desenhe e faça brainstorming

Use as ferramentas para esboçar ideias, adicionar notas adesivas, desenhar setas entre conceitos — tudo o que ajudar você a pensar. Este é o seu espaço.

![Passo 3 — Desenhe e faça brainstorming](../../skills/napkin/assets/step3-draw.svg)

### Passo 4: Compartilhe com o Copilot

Quando você quiser a contribuição do Copilot, clique no botão verde **Share with Copilot**. Ele salva uma captura de tela e copia suas notas.

![Passo 4 — Compartilhe com o Copilot](../../skills/napkin/assets/step4-share.svg)

### Passo 5: O Copilot responde

Volte ao seu terminal e diga `check the napkin`. O Copilot olha para o seu quadro branco — incluindo seus desenhos — e responde.

![Passo 5 — O Copilot responde](../../skills/napkin/assets/step5-response.svg)

## O que está incluído

### Skill

| Skill | Descrição |
|-------|-------------|
| `napkin` | Colaboração em quadro branco visual — cria um quadro branco, interpreta seus desenhos e notas e responde de forma conversacional |

### Ativos incluídos

| Ativo | Descrição |
|-------|-------------|
| `assets/napkin.html` | A aplicação de quadro branco — um único arquivo HTML que abre em qualquer navegador, sem necessidade de instalação |

## Recursos do quadro branco

| Recurso | O que faz |
|---------|-------------|
| **Desenho à mão livre** | Desenhe com uma ferramenta de caneta, como no papel |
| **Formas** | Retângulos, círculos, linhas e setas — formas trêmulas se ajustam a versões limpas |
| **Notas adesivas** | Notas arrastáveis, redimensionáveis e codificadas por cores (amarelo, rosa, azul, verde) |
| **Rótulos de texto** | Clique em qualquer lugar para digitar texto diretamente na tela |
| **Pan e zoom** | Segure a barra de espaço e arraste para se mover; role para dar zoom |
| **Undo/Redo** | Cometeu um erro? Ctrl+Z para desfazer, Ctrl+Shift+Z para refazer |
| **Auto-save** | Seu trabalho é salvo automaticamente — feche a aba, volte depois, ele continuará lá |
| **Share with Copilot** | Um botão exporta uma captura de tela e copia seu conteúdo de texto |

## Como o Copilot entende seus desenhos

Quando você clica em "Share with Copilot", duas coisas acontecem:

1. **Uma captura de tela é salva** (`napkin-snapshot.png` na sua pasta Downloads ou Desktop). O Copilot lê essa imagem e consegue ver tudo — esboços, setas, agrupamentos, anotações, notas adesivas, layout espacial.

2. **Seu texto é copiado para a área de transferência.** Isso fornece ao Copilot o texto exato das suas notas adesivas e rótulos, para que nada seja lido incorretamente a partir da imagem.

O Copilot usa ambos para entender o que você está pensando e responder como um colaborador — não como um computador analisando dados, mas como um colega olhando para o esboço do seu quadro branco.

## O que você pode desenhar?

Qualquer coisa. Mas aqui estão algumas coisas que o Copilot interpreta especialmente bem:

| O que você desenha | O que o Copilot entende |
|---------------|------------------------|
| Caixas conectadas por setas | Um fluxo de processo ou fluxo de trabalho |
| Itens circulados em conjunto | Um grupo de ideias relacionadas |
| Notas adesivas de cores diferentes | Categorias ou prioridades |
| Texto com uma linha atravessando | Algo rejeitado ou despriorizado |
| Estrelas ou pontos de exclamação | Itens de alta prioridade |
| Itens em lados opostos | Uma comparação ou contraste |
| Um organograma aproximado | Estrutura de reporte ou layout da equipe |

## Atalhos de teclado

Você não precisa deles — tudo funciona com cliques do mouse. Mas, se quiser trabalhar mais rápido:

| Tecla | Ferramenta |
|-----|------|
| V | Selecionar / mover |
| P | Caneta (desenhar) |
| R | Retângulo |
| C | Círculo |
| A | Seta |
| L | Linha |
| T | Texto |
| N | Nova nota adesiva |
| E | Borracha |
| Delete | Excluir item selecionado (ainda não suportado) |
| Ctrl+Z | Desfazer |
| Ctrl+Shift+Z | Refazer |
| Space + drag | Mover a tela |
| ? | Mostrar ajuda |

## Perguntas frequentes

**Preciso instalar algo além do plugin?**
Não. O quadro branco é um único arquivo HTML que abre no seu navegador. Sem apps, sem contas, sem configuração.

**Funciona offline?**
Sim. Tudo roda localmente no seu navegador. Não é necessária conexão com a internet para o quadro branco em si.

**Quais navegadores funcionam?**
Qualquer navegador moderno — Chrome, Safari, Edge, Firefox. O Chrome funciona melhor para o recurso "copy to clipboard".

**Posso salvar meu trabalho?**
Sim, automaticamente. O quadro branco salva no armazenamento local do seu navegador a cada poucos segundos. Feche a aba, volte depois, seu trabalho continuará lá.

**O Copilot realmente consegue entender meus desenhos?**
Sim. Os modelos de IA que alimentam o Copilot CLI (Claude, GPT) conseguem interpretar imagens. Eles podem ver seus esboços, ler seu texto em estilo manuscrito, entender relações espaciais e interpretar padrões visuais comuns, como fluxogramas, agrupamentos e anotações.

**E se eu não desenhar bem?**
Não importa. O quadro branco ajusta formas trêmulas para versões limpas, e o Copilot é treinado para interpretar esboços aproximados. Bonecos-palito e setas bagunçadas funcionam muito bem.

**Como começo de novo?**
Diga "let's napkin" novamente no CLI. O Copilot perguntará se você quer manter o quadro branco existente ou começar do zero.

**Quais plataformas são suportadas?**
macOS, Linux e Windows. O quadro branco roda em qualquer navegador. A integração com a área de transferência usa ferramentas nativas da plataforma (`pbpaste` no macOS, `xclip` no Linux, PowerShell no Windows).

## Origem

Este plugin faz parte do [Awesome Copilot](https://github.com/github/awesome-copilot), uma coleção orientada pela comunidade de extensões do GitHub Copilot.

## Licença

MIT
