FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

RUN pip install protobuf
RUN pip install kafka-python

COPY generator/order-generator.py /app
COPY protobuf/messages_pb2.py /app
COPY generator/data /app


CMD ["python", "/app/order-generator.py"]


