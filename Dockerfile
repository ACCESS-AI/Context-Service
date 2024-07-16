FROM python:3.10

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /usr/src/app/app

EXPOSE 3423

ENTRYPOINT [ "uvicorn", "app.main:app" ]

CMD [ "--host", "0.0.0.0", "--port", "3423"]






