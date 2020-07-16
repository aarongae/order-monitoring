import signal
import sys
import threading
import time
import csv

from kafka.errors import NoBrokersAvailable
from kafka import KafkaProducer

from messages_pb2 import OrderUpdate

KAFKA_BROKER = "kafka-broker:9092"
CSV_PATH = "ka-medium-1_orderStatus.csv"
DELAY = 1


def send_csv():
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])

    csv_file = open(CSV_PATH)
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        update = OrderUpdate()
        update.id = row["OrderId"]
        update.vehicle = row["VehicleId"]
        update.status = row["OrderStatus"]
        update.time = float(row["unix_timestamp"])
        key = update.id.encode('utf-8')
        val = update.SerializeToString()
        producer.send(topic='orders', key=key, value=val)
        producer.flush()
        time.sleep(DELAY)

    csv_file.close()


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

    producer = threading.Thread(target=safe_loop, args=[send_csv])
    producer.start()
    producer.join()


if __name__ == "__main__":
    main()
