FROM python:3.7

RUN mkdir -p /app
WORKDIR /app

RUN pip install dash
RUN pip install sqlalchemy
RUN pip install pymysql
RUN pip install pandas

COPY app.py /app

EXPOSE 8050

CMD ["python", "/app/app.py"]


