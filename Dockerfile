#Simple hello world flask app
FROM python:2.7

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python"]

CMD ["app.py"]
