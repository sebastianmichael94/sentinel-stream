# 🛡️ Sentinel Stream: Real-Time Fraud Detection System

A high-performance, event-driven banking security system built to simulate real-time fraud detection. This project demonstrates a full-stack asynchronous architecture using a "Producer-Broker-Consumer-Storage" pattern.

## Architecture Overview

The system is divided into four main layers:

1.  **Ingestion Layer**: A Python producer simulates live financial transactions and streams them into **Apache Kafka**.
2.  **Processing Layer**: A **FastAPI** background worker consumes the stream, applies fraud detection logic, and flags suspicious activity.
3.  **Persistence Layer**: Validated records and fraud alerts are stored in **PostgreSQL** using **SQLModel** (ORM) for long-term auditing.
4.  **Observation Layer**: A live **JavaScript Dashboard** fetches data from FastAPI endpoints to display real-time alerts to security analysts.

## Tech Stack

- **Language**: Python 3.10+
- **Stream Processing**: Apache Kafka (via `aiokafka`)
- **API Framework**: FastAPI (Asynchronous)
- **Database**: PostgreSQL & SQLModel (Pydantic + SQLAlchemy)
- **Infrastructure**: Docker & Docker Compose
- **Frontend**: HTML5, Bootstrap, and Vanilla JavaScript

## Key Learnings & Engineering Concepts

Throughout this project, I implemented several "Senior-level" backend concepts:

- **Distributed Offsets**: Learned how Kafka uses `group_id` and offsets to act as a "bookmark," ensuring that if the FastAPI consumer crashes, it resumes exactly where it left off without data loss.
- **Asynchronous Task Management**: Leveraged `asyncio` to run a continuous Kafka consumption loop in the background while simultaneously serving API requests on the same FastAPI instance.
- **Database Persistence vs. Streaming**: Understood the trade-off between ephemeral stream data (Kafka) and persistent relational data (Postgres) for historical auditing.
- **CORS & API Security**: Configured Cross-Origin Resource Sharing (CORS) middleware to allow the frontend dashboard to securely communicate with the backend.
- **Decoupled Logic**: Implemented a "Rules Engine" mindset where fraud logic is separated from the ingestion plumbing, making the system pluggable and scalable.

## How to Run

1.  **Start Infrastructure**:
    `docker compose up -d`
2.  **Run the Backend**:
    `uvicorn app.main:app --reload`
3.  **Start the Data Stream**:
    `python producer.py`
4.  **View Dashboard**:
    Open `frontend/index.html` in any browser.
