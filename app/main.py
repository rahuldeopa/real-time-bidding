from fastapi import FastAPI, WebSocket
from .database import SessionLocal, Bid
from .schemas import BidSchema
from .kafka_producer import publish_bid
from .websocket_manager import manager

app = FastAPI()

@app.post("/place_bid/")
async def place_bid(bid: BidSchema):
    db = SessionLocal()
    new_bid = Bid(auction_id=bid.auction_id, user_id=bid.user_id, amount=bid.amount)
    db.add(new_bid)
    db.commit()
    bid_data = bid.dict()
    publish_bid(bid_data)
    return {"status": "Bid placed successfully!"}

@app.websocket("/ws/bid_updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            pass  # Keep alive
    except:
        manager.disconnect(websocket)