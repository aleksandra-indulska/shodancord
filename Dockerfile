FROM python:3.10

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /bot

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY . .

CMD python3 main.py
