from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from fetch_emails import fetch_emails
from extract_insights import extract_insights
import uvicorn
import os
import json

app = FastAPI()

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/insights")
async def get_insights(date: str = Query(None)):
    print(f"Request received for date: {date}")
    
    # 1. Fetch Emails for specific date
    emails = fetch_emails(target_date=date)
    
    if not emails:
        return {"insights": []}

    # 2. Extract Insights
    enriched_data = extract_insights(emails)
    
    return {"insights": enriched_data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
