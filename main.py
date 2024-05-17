from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Initialize Firebase
cred = credentials.Certificate('IOT-Project.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define the data model for readings
class Reading(BaseModel):
    temp: float
    humidity: float
    motion: int
    water: float

@app.post("/reading")
async def create_reading(reading: Reading):
    try:
        # Create a new document in Firestore with an auto-generated ID
        doc_ref = db.collection('iot-db').document()
        doc_ref.set({
            'temp': reading.temp,
            'humidity': reading.humidity,
            'motion': reading.motion,
            'water': reading.water
        })
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

