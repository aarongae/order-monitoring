import signal
import sys
import time
import threading

import random

from kafka.errors import NoBrokersAvailable

from messages_pb2 import OrderUpdate, OrderStatus, Report

from kafka import KafkaProducer
from kafka import KafkaConsumer

KAFKA_BROKER = "kafka-broker:9092"
ORDER_ID = ["105047", "124686", "136861", "139901", "153463", "155573"]
VEHICLE_ID = ["-1", "1", "2", "3", "4", "5"]


def random_requests():
    """Generate infinite sequence of random OrderUpdates."""
    while True:
        request = OrderUpdate()
        request.id = random.choice(ORDER_ID)
        #request.vehicle = random.choice(VEHICLE_ID)
        yield request


def produce():
    delay_seconds = 1
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
    for request in random_requests():
        key = request.id.encode('utf-8')
        val = request.SerializeToString()
        producer.send(topic='orders', key=key, value=val)
        producer.flush()
        time.sleep(delay_seconds)


def consume():
    consumer = KafkaConsumer(
        'status',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest')
    for message in consumer:
        response = OrderStatus()
        response.ParseFromString(message.value)
        print("%s" % (response.status), flush=True)

def consume2():
    consumer2 = KafkaConsumer(
        'reports',
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest')
    for message in consumer2:
        response = Report()
        response.ParseFromString(message.value)

        tu = time.ctime(int(response.timeUnassigned))
        ta = time.ctime(int(response.timeAssigned))
        tp = time.ctime(int(response.timeInProgress))
        td = time.ctime(int(response.timeDelivered))

        print("Order:%s Vehicle:%d UNASSIGNED:%s ASSIGNED:%s IN_PROGRESS:%s DELIVERED:%s ThroughputTime:%s" 
            % (response.id, response.vehicle, response.timeUnassigned, response.timeAssigned, response.timeInProgress, response.timeDelivered, response.test), flush=True)


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

    producer = threading.Thread(target=safe_loop, args=[produce])
    producer.start()

    consumer = threading.Thread(target=safe_loop, args=[consume])
    consumer.start()

    consumer2 = threading.Thread(target=safe_loop, args=[consume2])
    consumer2.start()

    producer.join()
    consumer.join()
    consumer2.join()


if __name__ == "__main__":
    main()
