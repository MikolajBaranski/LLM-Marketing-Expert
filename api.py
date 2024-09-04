from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List
from PIL import Image
import io
from utils.experts import MarketingAgent

# Initialize agent and app
predict_helper = MarketingAgent()
app = FastAPI()

# Core app
@app.post("/upload/")
async def upload_run(image_raw: UploadFile = File(...), image_heatmap: UploadFile = File(...)):

    # Read images from file objects
    image_raw_data = await image_raw.read()
    image_heatmap_data = await image_heatmap.read()

    image_raw = Image.open(io.BytesIO(image_raw_data))
    image_heatmap = Image.open(io.BytesIO(image_heatmap_data))

    # Process images using your predict_helper
    result = predict_helper.full_agent_pipe(image_raw, image_heatmap)

    return result