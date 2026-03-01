# tolkien-retriever

Backend API para processamento de manuais de jogos de tabuleiro e chat com suporte a RAG.

## Requisitos

- Python 3.11+

## Instalação

Instalação padrão:

```bash
pip install -e .
```

Instalação com dependências de desenvolvimento:

```bash
pip install -e .[dev]
```

## Pre-commit

Instalar hooks:

```bash
pre-commit install
pre-commit install --hook-type pre-push
```

Rodar em todos os arquivos:

```bash
pre-commit run --all-files
```

## Executar a API

```bash
uvicorn src.main:app --reload --host 127.0.0.1 --port 8001
```

## Testes

```bash
pytest
```

## Formatação

```bash
black src tests
isort src tests
```
