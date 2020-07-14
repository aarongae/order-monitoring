import signal
import sys
import threading
from datetime import datetime
import time

from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer

from messages_pb2 import Report, Overview, TimeoutReport

KAFKA_BROKER = "kafka-broker:9092"


def consume():
    consumer = KafkaConsumer(
        'reports',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest')
    for message in consumer:
        response = Report()
        response.ParseFromString(message.value)

        print("Order:{} Vehicle:{} UNASSIGNED:{} ASSIGNED:{} IN_PROGRESS:{} DELIVERED:{} ThroughputTime:{}"
            .format(
            response.id, response.vehicle,
            datetime.utcfromtimestamp(response.timeUnassigned).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(response.timeAssigned).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(response.timeInProgress).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(response.timeDelivered).strftime('%Y-%m-%d %H:%M:%S'),
            str(datetime.utcfromtimestamp(response.timeDelivered) - datetime.utcfromtimestamp(response.timeUnassigned))
            ),
            flush=True
        )

def consume_overview():
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

def consume_timeout():
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
