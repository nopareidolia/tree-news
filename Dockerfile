FROM python:3.11-slim as os-base

ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install -y curl
WORKDIR /app

FROM os-base as poetry-base

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv

FROM os-base as main

ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry-base /app /app
CMD ["python", "-m", "tree_news"]