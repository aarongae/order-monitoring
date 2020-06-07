FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN pip install protobuf
RUN pip install kafka-python

COPY results-consumer.py /app
COPY messages_pb2.py /app


CMD ["python", "/app/results-consumer.py"]


