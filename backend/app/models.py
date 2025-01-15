from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Auction(Base):
    __tablename__ = "auctions"

    auction_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, index=True)
    status = Column(Enum('Live', 'Ended', name="auction_status"), default='Live')
    starting_price = Column(DECIMAL)
    bids = relationship("Bid", back_populates="auction")

class Bid(Base):
    __tablename__ = "bids"

    bid_id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey('auctions.auction_id'))
    user_id = Column(Integer)
    bid_amount = Column(DECIMAL)
    bid_time = Column(DateTime, default=datetime.utcnow)

    auction = relationship("Auction", back_populates="bids")
