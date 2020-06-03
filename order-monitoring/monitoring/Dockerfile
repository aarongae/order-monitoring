FROM python:3.7-alpine

RUN mkdir -p /app
WORKDIR /app

COPY apache_flink_statefun-snapshot-py3-none-any.whl /app
RUN pip install apache_flink_statefun-snapshot-py3-none-any.whl

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY monitoring.py /app
COPY messages_pb2.py /app

EXPOSE 8000


CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w 4", "monitoring:app"]

