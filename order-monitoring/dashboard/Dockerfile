FROM python:3.7

RUN mkdir -p /app
WORKDIR /app

RUN pip install dash
RUN pip install sqlalchemy
RUN pip install psycopg2
RUN pip install pandas
RUN pip install cryptography

COPY app.py /app

EXPOSE 8050

CMD ["python", "/app/app.py"]


