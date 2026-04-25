import json
import os
import time
from datetime import datetime, UTC

from confluent_kafka import Producer


def main() -> None:
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("KAFKA_TOPIC", "app-logs")
    interval = float(os.getenv("PRODUCE_INTERVAL_SECONDS", "1.0"))

    producer = Producer(
        {
            "bootstrap.servers": bootstrap_servers,
        }
    )

    def delivery_report(err, msg):
        if err is not None:
            print(f"Delivery failed: {err}")

    counter = 0
    while True:
        payload = {
            "service": "log-producer",
            "level": "INFO",
            "message": f"Generated event {counter}",
            "timestamp": datetime.now(UTC).isoformat(),
        }

        producer.produce(
            topic, json.dumps(payload).encode("utf-8"), callback=delivery_report
        )
        producer.poll(0)
        producer.flush()

        counter += 1
        time.sleep(interval)


if __name__ == "__main__":
    main()
