FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

COPY monitoring/apache_flink_statefun-snapshot-py3-none-any.whl /app
RUN pip install apache_flink_statefun-snapshot-py3-none-any.whl

COPY monitoring/requirements.txt /app
RUN pip install -r requirements.txt

COPY monitoring/monitoring.py /app
COPY protobuf/messages_pb2.py /app

EXPOSE 8000


CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w 4", "monitoring:app"]

