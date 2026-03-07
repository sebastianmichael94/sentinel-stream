from sqlmodel import SQLModel, create_engine, Session

# This URL matches the credentials you put in docker-compose.yml
sqlite_url = "postgresql://user:password@localhost:5432/sentinel_db"
engine = create_engine(sqlite_url, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session