from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List
from utils.agents import MarketingAgent

# Initialize agent and app
predict_helper = MarketingAgent()
app = FastAPI()

# Core app
@app.post("/upload/")
async def upload_run(files: List[UploadFile] = File(...)):
    if len(files) != 2:
        raise HTTPException(status_code=400, detail="Exactly two files must be uploaded")

    image_raw = files[0]
    image_heatmap = files[1]

    result = predict_helper.full_agent_pipe(image_raw, image_heatmap)

    return result