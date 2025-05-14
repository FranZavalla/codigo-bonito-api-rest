# Código Bonito - Product API

## Description

A small REST API to manage products. The objective is to show the good guidelines for creating pretty code and teach the different layers that a project has.

**NOTE**: This project is a refactoring of the original [project](https://github.com/matiaslee/testing_talk) created for various talks

## Requirements

- Python 3.10.12 or higher
- [Poetry](https://python-poetry.org/docs/)

---

## Installation

### 1. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3  -
```

Make sure `poetry` is in your PATH. You may need to restart your terminal.

### 2. Install dependencies

```bash
poetry install
```

This installs all project dependencies listed in `pyproject.toml`.

## Running the app

Make sure you are in the root of the project.
Create a `.env` file in the `app` folder with the following content:

```env
DATABASE_PATH=path_to_your_database.sqlite
ORM=sqlalchemy
# ORM=ponyorm
BLUELYTICS_API_URL=https://api.bluelytics.com.ar/v2/latest
```

Then run the following command at the root of the project to start the app:

```bash
poetry run uvicorn app.main:app --reload
```
