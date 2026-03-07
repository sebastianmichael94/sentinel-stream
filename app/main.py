import asyncio
import json
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
from sqlmodel import Session,select
from .database import init_db,engine
from .models import TransactionRecord
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sentinel Stream - Fraud Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any origin (fine for local dev)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start the listener when the app starts
@app.on_event("startup")
async def startup_event():
    init_db()
    # Create a background task so it doesn't block the API
    asyncio.create_task(consume_transactions())

async def consume_transactions():
    consumer = AIOKafkaConsumer(
        "transactions",
        bootstrap_servers='localhost:9092',
        group_id="fraud-detectors",
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    try:
        print("--- SENTINEL IS WATCHING THE STREAM ---")
        async for msg in consumer:
            tx_data = msg.value
            amount = tx_data.get('amount', 0)
            
            # 1. Apply Banking Logic
            is_fraud = amount > 9000
            reason = "High Value Transaction (Over $9k)" if is_fraud else "Valid"
            
            # 2. Create the Database Record
            record = TransactionRecord(
                **tx_data,
                is_fraud=is_fraud,
                fraud_reason=reason
            )

            # 3. Save to PostgreSQL
            with Session(engine) as session:
                session.add(record)
                session.commit()

            # 4. Professional Logging
            status = "⚠️ FRAUD DETECTED" if is_fraud else "✅ APPROVED"
            print(f"{status}: {tx_data['account_id']} | ${amount} | {reason}")
    finally:
        await consumer.stop()

@app.get("/")
def read_root():
    return {"status": "Sentinel is active and monitoring Kafka"}

@app.get("/transactions", response_model=list[TransactionRecord])
def get_all_transactions():
    """Returns the most recent 20 transactions processed"""
    with Session(engine) as session:
        # This is the line that fetches data from Postgres
        statement = select(TransactionRecord).order_by(TransactionRecord.processed_at.desc()).limit(20)
        results = session.exec(statement).all()
        return results