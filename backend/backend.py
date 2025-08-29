from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

# ------------------------------
# Initialize FastAPI
app = FastAPI(title="Real-Time Traffic Prediction API")

# Database setup
DATABASE_URL = "sqlite:///./traffic.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ------------------------------
# Database Model
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    horizon_min = Column(Integer)
    predicted_speed = Column(Float)
    metadata_json = Column(JSON)

Base.metadata.create_all(bind=engine)

# ------------------------------
# Request Model
class TrafficData(BaseModel):
    segment_id: str
    horizon_min: int
    predicted_speed: float
    model: str

# ------------------------------
# API Endpoints
@app.get("/health")
def health_check():
    return {"status": "✅ Backend is running!"}

@app.post("/predict")
def predict(item: TrafficData):
    db = SessionLocal()
    pr = Prediction(
        segment_id=item.segment_id,
        horizon_min=item.horizon_min,
        predicted_speed=item.predicted_speed,
        metadata_json={"model": item.model}
    )
    db.add(pr)
    db.commit()
    db.refresh(pr)
    db.close()
    return {"message": "Prediction stored successfully", "id": pr.id}

@app.get("/predictions")
def get_predictions():
    db = SessionLocal()
    data = db.query(Prediction).all()
    db.close()
    return data
