from pydantic import BaseModel

class BidSchema(BaseModel):
    auction_id: int
    user_id: int
    amount: float