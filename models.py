from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from database import Base
import datetime

class PaymentEvent(Base):
    __tablename__ = "payment_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False) # Ensures Idempotency 
    payment_id = Column(String, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    # Storing the full payload as JSON
    full_payload = Column(JSON, nullable=False)
    # Using the event's creation time or system receipt time
    received_at = Column(DateTime(timezone=True), server_default=func.now())