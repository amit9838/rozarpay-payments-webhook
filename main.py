from fastapi import FastAPI, Request, HTTPException, Depends, Header, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
from typing import Optional

from database import engine, Base, get_db
from models import PaymentEvent
from utils import verify_signature

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CiviRozarpay Payments Webhook")

# --- Endpoints ---
@app.post("/webhook/payments", status_code=status.HTTP_200_OK)
async def receive_webhook(
    request: Request,
    x_razorpay_signature: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Endpoint: POST /webhook/payments 
    Receives webhook calls, validates signature, and stores data.
    """
    
    # 1. Read Raw Body for Signature Verification
    try:
        raw_body = await request.body()
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to read request body")

    # 2. Validate Signature 
    if not x_razorpay_signature:
        raise HTTPException(status_code=403, detail="Missing Signature Header")
        
    if not verify_signature(raw_body, x_razorpay_signature):
        raise HTTPException(status_code=403, detail="Invalid Signature")

    # 3. Parse JSON 
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # 4. Extract Data
    # Based on Mock Payload structure: event, id, payload.payment.entity.id
    try:
        event_type = payload.get("event")
        event_id = payload.get("id")
        
        # Safe extraction of nested payment ID
        payment_data = payload.get("payload", {}).get("payment", {}).get("entity", {})
        payment_id = payment_data.get("id")

        if not all([event_type, event_id, payment_id]):
            raise ValueError("Missing required fields in payload")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Malformed Payload: {str(e)}")

    # 5. Store in DB & Handle Idempotency
    new_event = PaymentEvent(
        event_id=event_id,
        payment_id=payment_id,
        event_type=event_type,
        full_payload=payload
    )

    try:
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return {"status": "success", "message": "Event processed"}
    except IntegrityError:
        # Idempotency: If event_id exists, we rollback and return 200
        # or we could return 409 Conflict depending on preference.
        # Here we acknowledge receipt to stop webhook retries.
        db.rollback()
        return {"status": "ignored", "message": "Event already processed"}


@app.get("/payments/{payment_id}/events")
def get_payment_events(payment_id: str, db: Session = Depends(get_db)):
    """
    Endpoint: GET /payments/{payment_id}/events
    Returns all events related to a payment_id sorted by received_at.
    """
    events = db.query(PaymentEvent)\
        .filter(PaymentEvent.payment_id == payment_id)\
        .order_by(PaymentEvent.received_at.asc())\
        .all()

    # Format response as per example
    response_data = []
    for event in events:
        response_data.append({
            "event_type": event.event_type,
            "received_at": event.received_at.isoformat(),
        })
    
    return response_data