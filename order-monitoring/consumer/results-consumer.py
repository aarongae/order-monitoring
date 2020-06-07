import signal
import sys
import threading
import datetime
import time

from kafka.errors import NoBrokersAvailable
from kafka import KafkaConsumer

from messages_pb2 import Report

KAFKA_BROKER = "kafka-broker:9092"


def consume():
    consumer = KafkaConsumer(
        'reports',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest')
    for message in consumer:
        response = Report()
        response.ParseFromString(message.value)

        print("Order:{} Vehicle:{} UNASSIGNED:{} ASSIGNED:{} IN_PROGRESS:{} DELIVERED:{} ThroughputTime:{}".format(
            response.id, response.vehicle,
            datetime.utcfromtimestamp(response.timeUnassigned).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(response.timeAssigned).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(response.timeInProgress).strftime('%Y-%m-%d %H:%M:%S'),
            datetime.utcfromtimestamp(response.timeDelivered).strftime('%Y-%m-%d %H:%M:%S'),
            str(datetime.utcfromtimestamp(response.timeDelivered) - datetime.utcfromtimestamp(response.timeUnassigned))
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
    consumer.start()
    consumer.join()


if __name__ == "__main__":
    main()
