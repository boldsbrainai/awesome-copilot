---
applyTo: '**'
---
# SDK para Dataverse em Python — Começando

- Instale o SDK para Dataverse em Python e os pré-requisitos.
- Configure as variáveis de ambiente para o tenant do Dataverse, ID do cliente, segredo e URL de recurso.
- Utilize o SDK para autenticação via OAuth e realizar operações CRUD.

## Configuração
- Python 3.10+
- Recomendado: ambiente virtual

## Instalação
```bash
pip install dataverse-sdk
```

## Fundamentos da Autenticação
- Utilize OAuth com o registro de aplicativos do Azure AD.
- Armazene segredos em `.env` e carregue-os usando `python-dotenv`.

## Tarefas Comuns
- Consultar tabelas
- Criar/atualizar linhas
- Operações em lote
- Gerenciar paginação e throttling

## Dicas
- Reutilize os clientes; evite reautenticações frequentes.
- Adicione retries para falhas transitórias.
- Registre as requisições para solucionar problemas.