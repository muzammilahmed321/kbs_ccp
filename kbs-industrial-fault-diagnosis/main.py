from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import sys
import os

# Notebooks folder ka path explicitly add karein taake inference_engine mil sakay
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

try:
    from inference_engine import run_hybrid_industrial_inference  # type: ignore
except ImportError as e:
    print(f"Import Error: {e}")

app = FastAPI(
    title="Industrial Fault Diagnosis API",
    description="Backend API for running XGBoost + Knowledge Base hybrid inference engine.",
    version="1.0"
)

# Frontend ke sath connect karne ke liye CORS enable karein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend se aane walay data ka structure
class MachineDataInput(BaseModel):
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float
    machine_type: str

@app.get("/")
def home():
    return {"message": "Industrial Fault Diagnosis Backend is running successfully!"}

@app.post("/predict")
def predict_industrial_fault(data: MachineDataInput):
    try:
        # Data ko DataFrame mein convert karein taake inference engine ka .iloc wala masla hal ho jaye
        input_df = pd.DataFrame([{
            'Air temperature [K]': data.air_temperature,
            'Process temperature [K]': data.process_temperature,
            'Rotational speed [rpm]': data.rotational_speed,
            'Torque [Nm]': data.torque,
            'Tool wear [min]': data.tool_wear,
            'Type': data.machine_type
        }])
        
        # Inference function call karein (DataFrame pass kar ke)
        result = run_hybrid_industrial_inference(input_df)
        
        return {
            "status": "success",
            "prediction_result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))