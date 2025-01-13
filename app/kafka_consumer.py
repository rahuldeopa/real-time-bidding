from kafka import KafkaConsumer
import json
from .websocket_manager import manager

consumer = KafkaConsumer(
    'bid_events',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def consume_events():
    for message in consumer:
        manager.broadcast(message.value)