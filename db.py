from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite database for storing chat sessions
DATABASE_URL = "sqlite:///./sessions.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Table to store each user–bot interaction
class ChatSession(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    session_id = Column(String)
    user_message = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create table if it does not exist
Base.metadata.create_all(bind=engine)
