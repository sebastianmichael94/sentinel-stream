# Logic to simulate high-volume transaction flow with a default transactions model
# Uses aiokafka for asynchronous message production to ensure non-blocking performance
import asyncio
import json
import random
import uuid
from datetime import datetime, UTC # Use modern UTC
from aiokafka import AIOKafkaProducer
from app.models import Transaction

async def send_transactions():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        # Use a lambda that handles the serialization within the model
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        while True:
            # Generate fake transaction data
            data = Transaction(
                transaction_id=str(uuid.uuid4()),
                account_id=f"ACC-{random.randint(1000, 9999)}",
                amount=round(random.uniform(10.0, 10000.0), 2),
                merchant_id=f"MERCH-{random.randint(100, 500)}",
                timestamp=datetime.now(UTC) # Fixes DeprecationWarning
            )
            
            # .model_dump() is the modern replacement for .dict() in Pydantic V2
            # mode="json" converts the datetime to a string automatically!
            payload = data.model_dump(mode="json") 
            
            print(f"Sending: {data.account_id} - ${data.amount}")
            await producer.send_and_wait("transactions", payload)
            await asyncio.sleep(2) 
    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(send_transactions())