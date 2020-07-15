import signal
import sys
import threading
from datetime import datetime
import time

from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer
import pymysql

from messages_pb2 import Report

KAFKA_BROKER = "kafka-broker:9092"


def consume():
    db_connection = pymysql.connect(
        host="database",
        port="3306",
        user="user",
        password="password",
        db="lieferbot"
    )
    db_cursor = db_connection.cursor()
    query = "CREATE TABLE reports(order VARCHAR(255), vehicle VARCHAR(255), unassigned VARCHAR(255), " \
            "assigned VARCHAR(255), inprogress VARCHAR(255), delivered VARCHAR(255), throughput VARCHAR(255))"
    db_cursor.execute(query)
    db_connection.commit()
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

        query = "INSERT INTO reports (order, vehicle, unassigned, assigned, inprogress, delivered, throughput)" \
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        db_cursor.execute(query, (response.id, response.vehicle,
                                  str_unassigned, str_assigned, str_inprogress, str_delivered, str_throughput))
        db_connection.commit()


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
    consumer.start()
    consumer.join()


if __name__ == "__main__":
    main()
