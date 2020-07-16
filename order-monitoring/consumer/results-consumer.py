import signal
import sys
import threading
from datetime import datetime
import time

from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer
import psycopg2

from messages_pb2 import Report, Overview, TimeoutReport

KAFKA_BROKER = "kafka-broker:9092"


def consume():
    db_connection = psycopg2.connect(
        host="database",
        port="5432",
        user="user",
        password="password",
        database="lieferbot"
    )
    db_connection.autocommit = True
    db_cursor = db_connection.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS reports (
            orderid VARCHAR(255), 
            vehicle VARCHAR(255), 
            unassigned VARCHAR(255),
            assigned VARCHAR(255), 
            inprogress VARCHAR(255), 
            delivered VARCHAR(255), 
            throughput VARCHAR(255)
        )
        """
    db_cursor.execute(query)
    consumer = KafkaConsumer(
        'reports',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest')
    for message in consumer:
        response = Report()
        response.ParseFromString(message.value)

        str_unassigned = datetime.utcfromtimestamp(response.timeUnassigned).strftime('%Y-%m-%d %H:%M:%S')
        str_assigned = datetime.utcfromtimestamp(response.timeAssigned).strftime('%Y-%m-%d %H:%M:%S')
        str_inprogress = datetime.utcfromtimestamp(response.timeInProgress).strftime('%Y-%m-%d %H:%M:%S')
        str_delivered = datetime.utcfromtimestamp(response.timeDelivered).strftime('%Y-%m-%d %H:%M:%S')
        str_throughput = str(datetime.utcfromtimestamp(response.timeDelivered)
                             - datetime.utcfromtimestamp(response.timeUnassigned))

        print("Order:{} Vehicle:{} UNASSIGNED:{} ASSIGNED:{} IN_PROGRESS:{} DELIVERED:{} ThroughputTime:{}".format(
            response.id, response.vehicle, str_unassigned, str_assigned, str_inprogress, str_delivered, str_throughput),
            flush=True
        )

        query = "INSERT INTO reports (orderid, vehicle, unassigned, assigned, inprogress, delivered, throughput)" \
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        db_cursor.execute(query, (response.id, response.vehicle,
                                  str_unassigned, str_assigned, str_inprogress, str_delivered, str_throughput))


def consume_overview():
    db_connection = psycopg2.connect(
        host="database",
        port="5432",
        user="user",
        password="password",
        database="lieferbot"
    )
    db_connection.autocommit = True
    db_cursor = db_connection.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS overviews ( 
            unassigned INTEGER,
            assigned INTEGER, 
            inprogress INTEGER, 
            delivered INTEGER
        )
        """
    db_cursor.execute(query)
    consumer_overview = KafkaConsumer(
        'overviews',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest')
    for message in consumer_overview:
        response = Overview()
        response.ParseFromString(message.value)

        print("Overview: UNASSIGNED:{} ASSIGNED:{} IN_PROGRESS:{} DELIVERED:{}".format(
            response.noUnassigned, response.noAssigned, response.noInProgress, response.noDelivered
            ),
            flush=True
        )
        query = "INSERT INTO overviews (unassigned, assigned, inprogress, delivered) VALUES (%d, %d, %d, %d)"
        db_cursor.execute(query, (response.noUnassigned, response.noAssigned,
                                  response.noInProgress, response.noDelivered))


def consume_timeout():
    db_connection = psycopg2.connect(
        host="database",
        port="5432",
        user="user",
        password="password",
        database="lieferbot"
    )
    db_connection.autocommit = True
    db_cursor = db_connection.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS timeouts ( 
            orderid VARCHAR(255),
            status VARCHAR(255)
        )
        """
    db_cursor.execute(query)
    consumer_timeout = KafkaConsumer(
        'timeouts',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest')
    for message in consumer_timeout:
        response = TimeoutReport()
        response.ParseFromString(message.value)

        print("TIMEOUT Order:{} State:{}".format(
            response.orderId, response.order.status
            ),
            flush=True
        )
        query = "INSERT INTO overviews (orderid, status) VALUES (%s, %s)"
        db_cursor.execute(query, (response.orderId, response.order.status))


def handler(number, frame):
    sys.exit(0)


def safe_loop(fn):
    while True:
        try:
            fn()
        except SystemExit:
            print("Good bye!")
            return
        except NoBrokersAvailable:
            time.sleep(2)
            continue
        except Exception as e:
            print(e)
            return


def main():
    signal.signal(signal.SIGTERM, handler)

    consumer = threading.Thread(target=safe_loop, args=[consume])
    consumer_overview = threading.Thread(target=safe_loop, args=[consume_overview])
    consumer_timeout = threading.Thread(target=safe_loop, args=[consume_timeout])

    consumer.start()
    consumer_overview.start()
    consumer_timeout.start()

    consumer.join()
    consumer_overview.join()
    consumer_timeout.start()


if __name__ == "__main__":
    main()
