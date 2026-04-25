import json
import os

from confluent_kafka import Consumer


def main() -> None:
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "app-logs")
    group_id = os.getenv("KAFKA_GROUP_ID", "log-consumer-group")

    consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            msg_value = msg.value()
            if msg_value is None:
                continue

            value = json.loads(msg_value.decode("utf-8"))
            print(json.dumps(value, ensure_ascii=True))
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
