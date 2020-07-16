FROM python:3.7-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN mkdir -p /app
WORKDIR /app

RUN pip install protobuf
RUN pip install kafka-python
RUN pip install psycopg2

COPY results-consumer.py /app
COPY messages_pb2.py /app


CMD ["python", "/app/results-consumer.py"]


