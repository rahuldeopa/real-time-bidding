from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from .websocket_manager import manager  # WebSocketManager class

# Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'kafka:9092',  # Kafka broker URL
    'group.id': 'bid_consumer_group',    # Consumer group ID
    'auto.offset.reset': 'earliest'      # Start from the earliest message
}

# Create Kafka Consumer instance
consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic where bids are being published
consumer.subscribe(['bids_topic'])  # Use the correct Kafka topic

def consume_bids():
    """ Continuously consume messages from Kafka and handle them. """
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Poll for new messages

            if msg is None:
                continue  # No message, continue polling

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition reached
                    print(f"End of partition reached: {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                else:
                    # Other error
                    raise KafkaException(msg.error())
            else:
                # Message successfully received, handle it
                print(f"Received message: {msg.value().decode('utf-8')}")

                # Deserialize the bid data from the message
                bid_data = json.loads(msg.value().decode('utf-8'))

                # Broadcast the bid update to WebSocket clients
                if bid_data:
                    # Broadcast bid update to all WebSocket clients
                    manager.broadcast_bid_update(bid_data)

    except KeyboardInterrupt:
        print("Consumer interrupted")

    finally:
        # Close the consumer when done
        consumer.close()
