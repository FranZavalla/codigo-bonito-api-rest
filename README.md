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

Make sure you are in the root folder (`/src`) of the project.
Create a `.env` file in the root folder with the following content:

```env
ENV=development
#production is also a valid option
```

Then run the following command to start the app:

```bash
poetry run uvicorn main:app --reload
```
