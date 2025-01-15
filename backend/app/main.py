from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Bid, Auction
from .schemas import BidSchema
from .database import SessionLocal, engine
from .kafka_producer import publish_bid
from .websocket_manager import manager
from app.database import SessionLocal, engine


app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/place_bid/")
async def place_bid(bid: BidSchema, db: Session = Depends(get_db)):
    # Retrieve auction from the database to ensure it's active
    auction = db.query(Auction).filter(Auction.auction_id == bid.auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.status == "Ended":
        raise HTTPException(status_code=400, detail="Auction has ended")

    # Create a new bid entry in the database
    new_bid = Bid(auction_id=bid.auction_id, user_id=bid.user_id, amount=bid.amount)
    db.add(new_bid)
    db.commit()

    # Send bid data to Kafka for real-time updates
    bid_data = bid.dict()
    publish_bid(bid_data)

    # Send real-time updates to all connected WebSocket clients
    await manager.broadcast_bid_update(bid_data)

    return {"status": "Bid placed successfully!"}

@app.websocket("/ws/bid_updates")
async def websocket_endpoint(websocket: WebSocket):
    # Handle new WebSocket connections
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
