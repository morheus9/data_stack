import json
import os
import time
from datetime import datetime, UTC

from kafka import KafkaProducer


def main() -> None:
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "app-logs")
    interval = float(os.getenv("PRODUCE_INTERVAL_SECONDS", "1.0"))

    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )

    counter = 0
    while True:
        payload = {
            "service": "log-producer",
            "level": "INFO",
            "message": f"Generated event {counter}",
            "timestamp": datetime.now(UTC).isoformat(),
        }
        producer.send(topic, payload)
        producer.flush()
        counter += 1
        time.sleep(interval)


if __name__ == "__main__":
    main()
