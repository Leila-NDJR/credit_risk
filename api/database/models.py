from sqlalchemy import Column, String, Float, DateTime, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ScoringEvent(Base):
    __tablename__ = "scoring_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    probability_default = Column(Float, nullable=False)
    decision = Column(String, nullable=False)

    features = Column(JSON, nullable=False)
    shap_values = Column(JSON, nullable=False)
