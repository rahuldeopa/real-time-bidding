from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Bid, Auction
from .schemas import BidSchema
from app.database import SessionLocal, engine
from app.kafka_producer import publish_bid
from .websocket_manager import manager
from app.database import SessionLocal, engine,Base
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

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
    db.refresh(new_bid)

     # 3. Publish to Kafka (Real-time Updates)
    bid_data = {
        "auction_id": bid.auction_id,
        "user_id": bid.user_id,
        "amount": bid.amount
    }
    try:
        publish_bid(bid_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish bid: {e}")

    # 4. Notify WebSocket Clients
    try:
        await manager.broadcast_bid_update(bid_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"WebSocket update failed: {e}")

    # 5. Return Response
    return {
        "status": "Bid placed successfully!",
        "bid": {
            "auction_id": new_bid.auction_id,
            "user_id": new_bid.user_id,
            "amount": new_bid.amount
        }
    }

@app.websocket("/ws/bid_updates")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)