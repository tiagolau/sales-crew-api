from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew import SalesCrew
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sales Follow-up Crew API")

class FollowUpRequest(BaseModel):
    client_name: str
    pain_points: str
    meeting_date: str
    # Optional context
    company_name: str = "Unknown Company"

class FollowUpResponse(BaseModel):
    message: str
    status: str

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Sales Crew API"}

@app.post("/generate-followup", response_model=FollowUpResponse)
def generate_followup(request: FollowUpRequest):
    try:
        # Initialize the Crew with request data
        crew = SalesCrew(
            client_name=request.client_name,
            pain_points=request.pain_points,
            meeting_date=request.meeting_date,
            company_name=request.company_name
        )
        
        result = crew.run()
        
        return FollowUpResponse(
            message=result,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
