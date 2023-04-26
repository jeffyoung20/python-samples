FROM python:3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/FastApiSqlAlchemy

CMD ["uvicorn", "FastApiSqlAlchemy.Main:app", "--host", "0.0.0.0", "--port", "80"]

