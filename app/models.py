from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    bid_amount = Column(Float, nullable=False)