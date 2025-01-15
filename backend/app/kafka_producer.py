from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def publish_bid(bid_data):
    producer.send('auction_bids', value=bid_data)
