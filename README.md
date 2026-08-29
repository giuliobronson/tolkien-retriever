# tolkien-retriever

Backend API para processamento de manuais de jogos de tabuleiro e chat com suporte a RAG.

## Requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) para gerenciamento de dependências

## Instalação

```bash
uv sync
```

Isso cria o `.venv` e instala as dependências travadas no `uv.lock` (inclui o grupo `dev`).

Para instalar sem as dependências de desenvolvimento:

```bash
uv sync --no-dev
```

### Alterar dependências

Edite `pyproject.toml` (`[project.dependencies]` ou `[dependency-groups]`) e rode:

```bash
uv lock       # regenera o uv.lock
uv sync       # aplica no .venv
```

## Pre-commit

Instalar hooks:

```bash
uv run pre-commit install
uv run pre-commit install --hook-type pre-push
```

Rodar em todos os arquivos:

```bash
uv run pre-commit run --all-files
```

## Executar a API

```bash
uv run uvicorn main:app --app-dir src --reload --host 127.0.0.1 --port 8001
```

## Docker

Stack completa (API + MinIO + MongoDB + Qdrant):

```bash
docker compose up -d --build
```

A API sobe em `http://localhost:8001`. O serviço `api` lê o `.env` (`env_file`) e
monta `./secrets` em `/app/secrets` para o JSON do Firebase — nada é embutido na
imagem; as URLs de MongoDB/MinIO/Qdrant são sobrescritas para os nomes de serviço
do compose.

Só a imagem:

```bash
docker build -t tolkien-retriever .
```
