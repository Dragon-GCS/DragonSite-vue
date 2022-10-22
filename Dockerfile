FROM python:slim
MAINTAINER Dragon-GCS

COPY ./server /app/server
COPY ./pyproject.toml /app/pyproject.toml

WORKDIR /app

RUN pip3 install -e .

CMD ["python3", "-m", "server", "-b", "0.0.0.0", "-p", "8080"]
