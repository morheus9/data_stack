import json
import os

from kafka import KafkaConsumer


def main() -> None:
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "app-logs")
    group_id = os.getenv("KAFKA_GROUP_ID", "log-consumer-group")

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset="earliest",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    for message in consumer:
        print(json.dumps(message.value, ensure_ascii=True))


if __name__ == "__main__":
    main()
