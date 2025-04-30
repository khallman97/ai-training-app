### FastAPI Backend Starter (main.py)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date, timedelta
from typing import Optional
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

app = FastAPI()

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Models ===
class User(BaseModel):
    id: int
    name: str
    sport: str
    training_days: List[str]
    long_days: List[str]
    goal: str
    goal_date: str
    start_date: str

class PlanItem(BaseModel):
    date: str
    title: str
    sport: Optional[str] = None
    description: Optional[str] = None
    expected_duration: str
    warmup: str
    main_set: str
    cooldown: str

# In-memory storage for now
users = {}
plans = {}

@app.post("/users", response_model=User)
def create_user(user: User):
    users[user.id] = user
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.get("/plans/{user_id}", response_model=List[PlanItem])
def get_plan(user_id: int):
    return plans.get(user_id, [])


@app.post("/plans/generate")
def generate_plan(user_id: int):
    user = users.get(user_id)
    if not user:
        return {"error": "user not found"}
    llm_res = call_open_ai_mock(user) # for testing this generates a premade plan to save api costs
    #llm_res = call_openai_to_generate_plan(user) # real command 
    #print(llm_res)
    today = date.today()
    training_plan = []
    for day in llm_res:
        print(day)
        for planned_workout in day['workouts']:
            print(planned_workout)
            workout = {
                "date": day['date'],
                "title": f"{planned_workout['sport']}",
                "sport": f"{planned_workout['sport']}", 
                "description": f"{planned_workout['description']}",
                "expected_duration": f"{planned_workout['expected_duration']}",
                "warmup": f"{planned_workout.get('warmup', 'N/a')}",
                "main_set": f"{planned_workout.get('main_set', 'N/a')}",
                "cooldown":  f"{planned_workout.get('cooldown', 'N/a')}"
            }
            training_plan.append(workout)

    plans[user_id] = training_plan
    #return training_plan
    return {"status": "plan generated"}

def call_open_ai_mock(user_input) -> list:
    with open('sample_data.json', 'r') as file:
        data = json.load(file)
    return data

def call_openai_to_generate_plan(user_input) -> list:
    print(f"user intput {user_input}")
    system_prompt = """You are a helpful assistant that generates training plans. You will have to generate a plan based around there race date and 
    should be based on a 3 week build one week recover scendule. Each workout should include:
    - sport (e.g., swim, bike, run)
    - description
    - expected_duration (e.g., "45 mins")
    - warmup, main_set, cooldown
    - if possible provide an expected TSS
    - if the workout is interval based include how long the rests/recoveries are
    - use zones to represent the workouts. For running use zone (1-5) heart rate or pace, for swimming use zone 1-5 based of crticial swim speed, for biking use zone 1-5 based on power or heart rate

    Return a JSON array of workouts, you can have multiple for a given day as well but it should be noted if its morning or afternoon or they should be done together
    (i.e brick session), starting with the given start_date.
    If a field is not applicable, set it to "n/a".
    """

    user_prompt = f"""
    Create a  {user_input.sport} training plan starting from {user_input.start_date}.
    The user wants to train for a {user_input.goal} on {user_input.goal_date}.
    Current long workout days: {user_input.long_days}. Only plan workouts on these days: {user_input.training_days}

    Make sure to include variety and structure: interval days, long sessions, rest if needed. Long sessions should be on the long workout days. 
    Respond only in JSON list format, Do not wrap it in markdown and add no comments anywhere, this should just be a json list.
    """
    open_api_key = os.getenv("OPENAI_API_KEY")
    #print(open_api_key)
    client = OpenAI(api_key= open_api_key)
    response = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
    )

    reply = response.choices[0].message.content
    print(reply)
    # Parse the response to a list (ideally OpenAI returns a JSON list)

    res = json.loads(reply)
    
    return json.loads(reply)
