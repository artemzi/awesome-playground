Ниже рабочий сетап под `uv` в стиле «минимум магии, максимум повторяемости». [realpython](https://realpython.com/python-uv/)

## Установка uv и Python

- Поставить `uv` по оф. инструкции (одна команда, см. install‑guide). [docs.astral](https://docs.astral.sh/uv/getting-started/installation/)
- Можно не ставить Python руками: `uv` сам подтянет нужную версию при первом запуске или через `uv python install 3.12`. [docs.astral](https://docs.astral.sh/uv/guides/install-python/)

Пример (Linux/macOS, из доки):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Шаблон проекта (API/скрипт)

Предположим, новый сервис `awesome-service`:

```bash
mkdir awesome-service
cd awesome-service

# Инициализируем проект (интерактивно задаст имя и версию)
uv init --app --python 3.12
```

Команда создаст `pyproject.toml`, `main.py` и `.venv` будет создаваться автоматически при `uv run`/`uv sync`. [uv.pydevtools](https://uv.pydevtools.com)

Для более «пакетного» стиля (src‑layout):

```bash
uv init --lib --python 3.12
# будет src/awesome_service/, удобно для больших сервисов
```

## Добавление зависимостей

Базовый стек (пример для FastAPI + uvicorn + тесты):

```bash
# runtime-зависимости
uv add fastapi uvicorn[standard]

# dev-зависимости
uv add --dev pytest pytest-cov ruff mypy
```

`uv` обновит `pyproject.toml` и `uv.lock`, а пакеты поставит в `.venv` рядом с проектом. [mlops-coding-course.fmind](https://mlops-coding-course.fmind.dev/1.%20Initializing/1.3.%20uv%20(project).html)

Синхронизация окружения по `pyproject.toml`/`uv.lock`:

```bash
uv sync
```

(Аналог `pip install -r requirements.txt`, только декларативно и с lock‑файлом.) [mlops-coding-course.fmind](https://mlops-coding-course.fmind.dev/1.%20Initializing/1.3.%20uv%20(project).html)

## Запуск и команды

- Локальный запуск приложения:

```bash
uv run python -m awesome_service   # если есть пакет
uv run python main.py              # если однофайловый скрипт
```

- Запуск FastAPI:

```bash
uv run uvicorn awesome_playground.awesome_service:app --reload
```

- Тесты и линтеры:

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```

`uv run` сам активирует нужную `.venv`, не нужно `source .venv/bin/activate`. [youtube](https://www.youtube.com/watch?v=AMdG7IjgSPM)

## Структура проекта

Типичный вид для lib/сервиса:

```text
awesome-service/
  src/
    awesome_service/
      __init__.py
      app.py          # FastAPI / core
      config.py
      services/...
  tests/
    test_app.py
  pyproject.toml
  uv.lock
  .venv/              # создаёт uv, в .gitignore
```

`pyproject.toml` описывает метаданные проекта, зависимости и entry‑points, `uv.lock` фиксирует точные версии. [realpython](https://realpython.com/python-uv/)

## Для CI/CD

- В CI достаточно:

```bash
uv sync --frozen     # использовать только версии из uv.lock
uv run pytest
```

- Кешировать можно директории `.venv` и кеш пакетов `uv` (из доки/примеров). [realpython](https://realpython.com/python-uv/)

***

Ruff и mypy — ключевые инструменты для качества кода: ruff заменяет линтеры/форматтеры вроде flake8/isort/black (быстрый, на Rust), mypy добавляет статическую проверку типов (ловит ошибки до запуска). [blog.csdn](https://blog.csdn.net/gitblog_00376/article/details/151249103)

## Зачем они нужны

- **Ruff**: Линтинг (стиль, ошибки, антипаттерны), автофикс, форматирование. Ускоряет ревью, снижает баги от стиля. Заменяет 5–10 тулов, работает в 10–100x быстрее flake8. [higherpass](https://www.higherpass.com/2025/04/29/enhancing-python-code-quality-with-ruff-black-and-mypy/)
- **Mypy**: Проверяет типы (int вместо str и т.п.), как TypeScript для Python. С `strict=true` — жёсткий режим для enterprise. Ловит 30–50% runtime‑ошибок на этапе dev. [zenn](https://zenn.dev/japan/articles/67ea057369d88e)

Вместе — дефолтный стек для команд в 2026: чистый код + типобезопасность без runtime‑сюрпризов. [discuss.python](https://discuss.python.org/t/starting-a-new-python-project-do-i-need-all-these-tools/105342)

## Как добавить в uv

```bash
uv add --dev ruff mypy
```

Это добавит их в `[tool.uv.dev-dependencies]` в `pyproject.toml`, обновит `uv.lock` и поставит в `.venv`. [emasuriano](https://emasuriano.com/blog/2025-01-21-simplifying-python-development-with-uv-a-modern-package-management-tool/)

После правок:

```bash
uv sync  # Синхронизирует dev-зависимости
```

## Команды для работы

```bash
# Ruff: линтинг + автофикс + форматирование
uv run ruff check . --fix
uv run ruff format .

# Mypy: типы
uv run mypy .

# Всё разом (в Makefile или pre-commit)
uv run ruff check . --fix && uv run ruff format . && uv run mypy .
```

## Pre-commit

```bash
# Добавить pre-commit в dev-зависимости
uv add --dev pre-commit

# Установить hooks
uv run pre-commit install

# Запустить вручную
uv run pre-commit run --all-files
```
