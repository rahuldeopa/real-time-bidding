from sqlalchemy import Column, Integer, String, Float, ForeignKey  # ✅ Added Float here
from sqlalchemy.orm import relationship
from app.database import Base

class Auction(Base):
    __tablename__ = "auctions"

    auction_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)
    starting_price = Column(Float, nullable=False)  # ✅ Uses Float
    status = Column(String(50), nullable=False, default="Live")

    bids = relationship("Bid", back_populates="auction")

class Bid(Base):
    __tablename__ = "bids"

    bid_id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.auction_id"))
    user_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)  # ✅ Uses Float

    auction = relationship("Auction", back_populates="bids")
