FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN pip install protobuf
RUN pip install kafka-python

COPY consumer/results-consumer.py /app
COPY protobuf/messages_pb2.py /app


CMD ["python", "/app/results-consumer.py"]


