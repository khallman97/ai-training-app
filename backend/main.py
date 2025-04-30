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
    llm_res = call_openai_to_generate_plan(user)
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
    return [{'date': '2025-04-23', 'workouts': [{'time_of_day': 'Morning', 'sport': 'Run', 'description': 'Interval Training', 'expected_duration': '1 hour', 'warmup': '10 mins easy jog', 'main_set': '5 x 1km at Zone 4 pace with 2 mins rest in between', 'cooldown': '10 mins easy jog', 'tss': 60}, {'time_of_day': 'Afternoon', 'sport': 'Swim', 'description': 'Technique Focus', 'expected_duration': '45 mins', 'warmup': '200m easy swim', 'main_set': '4 x 50m drills', 'cooldown': '200m easy swim', 'tss': 40}]}, {'date': '2025-04-24', 'workouts': [{'time_of_day': 'Morning', 'sport': 'Bike', 'description': 'Long Ride', 'expected_duration': '2.5 hours', 'warmup': '20 mins easy spin', 'main_set': 'Maintain Zone 2 with rolling hills', 'cooldown': '20 mins easy spin', 'tss': 150}]}, {'date': '2025-04-25', 'workouts': [{'time_of_day': 'Morning', 'sport': 'Rest', 'description': 'Active Recovery Day', 'expected_duration': 'n/a', 'warmup': 'n/a', 'main_set': 'n/a', 'cooldown': 'n/a'}]}, {'date': '2025-04-26', 'workouts': [{'time_of_day': 'Morning', 'sport': 'Swim', 'description': 'Threshold Swim', 'expected_duration': '1 hour', 'warmup': '200m easy swim', 'main_set': '4 x 200m at Zone 3 with 20 secs rest', 'cooldown': '200m easy swim', 'tss': 50}, {'time_of_day': 'Afternoon', 'sport': 'Run', 'description': 'Easy Run', 'expected_duration': '45 mins', 'warmup': '10 mins easy jog', 'main_set': 'Maintain Zone 2', 'cooldown': '10 mins easy jog', 'tss': 40}]}, {'date': '2025-04-27', 'workouts': [{'time_of_day': 'Morning', 'sport': 'Bike', 'description': 'Interval Training', 'expected_duration': '1.5 hours', 'warmup': '15 mins easy spin', 'main_set': '5 x 5 mins at Zone 4 with 3 mins rest in between', 'cooldown': 
'15 mins easy spin', 'tss': 90}]}, {'date': '2025-04-28', 'workouts': [{'time_of_day': 'Morning', 'sport': 'Run', 
'description': 'Tempo Run', 'expected_duration': '1 hour', 'warmup': '10 mins easy jog', 'main_set': '30 mins at Zone 3 pace', 'cooldown': '10 mins easy jog', 'tss': 60}]}]

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
    import json
    return json.loads(reply)
