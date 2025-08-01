from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional, List
from app.core.database import get_db
from app.models.auth import User
from app.models.training_plans import TrainingPlan
from app.api.auth import verify_token
from app.core.security import security_scheme

# Router
router = APIRouter(tags=["Training Plans"])

# Pydantic models
class TrainingPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # Running, Cycling, Triathlon
    start_date: date
    event_date: date
    skill_level: str  # beginner, intermediate, master
    long_days: List[str]  # List of days for long training sessions
    running_threshold_pace: Optional[str] = None  # Time format: "5:00 per km"
    biking_fpt: Optional[int] = None  # Functional Power Threshold
    critical_swim_speed: Optional[str] = None  # Time format: "2:05 per 100m"
    plan_type: Optional[str] = None  # Legacy field
    duration_weeks: Optional[int] = None  # Legacy field

class TrainingPlanCreate(TrainingPlanBase):
    @classmethod
    def validate_training_plan(cls, **data):
        """Validate training plan data"""
        # Validate type
        valid_types = ["Running", "Cycling", "Triathlon"]
        if data.get("type") not in valid_types:
            raise ValueError(f"type must be one of: {valid_types}")

        # Validate skill level
        valid_skill_levels = ["beginner", "intermediate", "master"]
        if data.get("skill_level") not in valid_skill_levels:
            raise ValueError(f"skill_level must be one of: {valid_skill_levels}")

        # Validate plan_type (goal) based on type
        plan_type = data.get("plan_type")
        if plan_type:
            valid_goals = {
                "Running": ["5k", "10k", "Half marathon", "Marathon", "Ultra"],
                "Cycling": ["Century", "Time trial"],
                "Triathlon": ["sprint", "olympic", "half distance", "full distance"]
            }
            training_type = data.get("type")
            if training_type in valid_goals and plan_type not in valid_goals[training_type]:
                raise ValueError(f"Invalid goal for {training_type}: {plan_type}. Must be one of: {valid_goals[training_type]}")

        # Validate long_days
        valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        long_days = data.get("long_days", [])
        if not isinstance(long_days, list):
            raise ValueError("long_days must be a list")
        for day in long_days:
            if day.lower() not in valid_days:
                raise ValueError(f"Invalid day in long_days: {day}. Must be one of: {valid_days}")

        # Validate dates
        start_date = data.get("start_date")
        event_date = data.get("event_date")
        if start_date and event_date and start_date >= event_date:
            raise ValueError("start_date must be before event_date")

        return cls(**data)

class TrainingPlanResponse(TrainingPlanBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    additional_data: Optional[dict] = None

    class Config:
        from_attributes = True

class TrainingPlanStatus(BaseModel):
    has_active_plan: bool
    active_plan: Optional[TrainingPlanResponse] = None

# Relationship is now defined in the User model

# Dependency to get current user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
):
    try:
        email = verify_token(credentials.credentials)
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# API endpoints
@router.get("/status", response_model=TrainingPlanStatus, tags=["Training Plans"])
async def get_training_plan_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if the current user has an active training plan
    """
    active_plan = db.query(TrainingPlan).filter(
        TrainingPlan.user_id == current_user.id,
        TrainingPlan.is_active == True
    ).first()
    
    return TrainingPlanStatus(
        has_active_plan=active_plan is not None,
        active_plan=active_plan
    )

@router.get("/", response_model=List[TrainingPlanResponse], tags=["Training Plans"])
async def get_training_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all training plans for the current user
    """
    plans = db.query(TrainingPlan).filter(
        TrainingPlan.user_id == current_user.id
    ).all()
    return plans

@router.post("/", response_model=TrainingPlanResponse, tags=["Training Plans"])
async def create_training_plan(
    plan: TrainingPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new training plan for the current user
    """
    try:
        # Validate the training plan data
        validated_plan = TrainingPlanCreate.validate_training_plan(**plan.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Deactivate any existing active plans
    existing_active = db.query(TrainingPlan).filter(
        TrainingPlan.user_id == current_user.id,
        TrainingPlan.is_active == True
    ).all()

    for existing_plan in existing_active:
        existing_plan.is_active = False

    # Calculate duration in weeks
    duration_days = (validated_plan.event_date - validated_plan.start_date).days
    duration_weeks = max(1, duration_days // 7)  # At least 1 week

    # Create new plan
    db_plan = TrainingPlan(
        user_id=current_user.id,
        name=validated_plan.name,
        description=validated_plan.description,
        type=validated_plan.type,
        start_date=validated_plan.start_date,
        event_date=validated_plan.event_date,
        skill_level=validated_plan.skill_level,
        long_days=validated_plan.long_days,
        running_threshold_pace=validated_plan.running_threshold_pace,
        biking_fpt=validated_plan.biking_fpt,
        critical_swim_speed=validated_plan.critical_swim_speed,
        plan_type=validated_plan.plan_type,  # Legacy field
        duration_weeks=duration_weeks,  # Calculate automatically
        is_active=True
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.put("/{plan_id}/activate", response_model=TrainingPlanResponse, tags=["Training Plans"])
async def activate_training_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activate a specific training plan
    """
    # Get the plan
    plan = db.query(TrainingPlan).filter(
        TrainingPlan.id == plan_id,
        TrainingPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    
    # Deactivate all other plans
    db.query(TrainingPlan).filter(
        TrainingPlan.user_id == current_user.id,
        TrainingPlan.is_active == True
    ).update({"is_active": False})
    
    # Activate this plan
    plan.is_active = True
    db.commit()
    db.refresh(plan)
    
    return plan

@router.put("/{plan_id}", response_model=TrainingPlanResponse, tags=["Training Plans"])
async def update_training_plan(
    plan_id: int,
    plan_update: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a training plan (for threshold updates)
    """
    plan = db.query(TrainingPlan).filter(
        TrainingPlan.id == plan_id,
        TrainingPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    
    # Update only the threshold fields
    if plan_update.get("running_threshold_pace") is not None:
        plan.running_threshold_pace = plan_update["running_threshold_pace"]
    
    if plan_update.get("biking_fpt") is not None:
        plan.biking_fpt = plan_update["biking_fpt"]
    
    if plan_update.get("critical_swim_speed") is not None:
        plan.critical_swim_speed = plan_update["critical_swim_speed"]
    
    db.commit()
    db.refresh(plan)
    
    return plan

@router.delete("/{plan_id}", tags=["Training Plans"])
async def delete_training_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a training plan
    """
    plan = db.query(TrainingPlan).filter(
        TrainingPlan.id == plan_id,
        TrainingPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    
    db.delete(plan)
    db.commit()
    
    return {"message": "Training plan deleted successfully"} 