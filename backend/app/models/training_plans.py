from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Date, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # New training plan fields
    type = Column(String, nullable=False)  # Running, Cycling, Triathlon
    start_date = Column(Date, nullable=False)
    event_date = Column(Date, nullable=False)
    skill_level = Column(String, nullable=False)  # beginner, intermediate, master
    long_days = Column(JSON, nullable=False)  # List of days for long training sessions
    running_threshold_pace = Column(String, nullable=True)  # Time format: "5:00 per km"
    biking_fpt = Column(Integer, nullable=True)  # Functional Power Threshold
    critical_swim_speed = Column(String, nullable=True)  # Time format: "2:05 per 100m"
    plan_type = Column(String, nullable=True)  # represents the sub event (ie half marathon, full marathon, ironman, etc)
    
    # Legacy fields (keeping for backward compatibility)
    duration_weeks = Column(Integer, nullable=True)

    # Additional metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Additional fields stored as JSON for future extensibility
    additional_data = Column(JSON, nullable=True)

    # Relationship to user
    user = relationship("User", back_populates="training_plans") 