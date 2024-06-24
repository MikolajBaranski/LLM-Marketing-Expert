# Load base image
FROM python:3.10-slim

# Upgrade pip
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /llm-pipeline

# Perfrom all installations for environment
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set environment variable for Hugging Face cache
ENV HF_HOME=/root/.cache/huggingface

# Create a script to download the model
RUN echo "from transformers import pipeline\n\
model_id = 'llava-hf/llava-1.5-7b-hf'\n\
pipe = pipeline('image-to-text', model=model_id)\n\
print('Model downloaded and cached successfully.')" > download_model.py

# Run the script to download the model and cache it during the build
RUN python download_model.py

# Copy all files from directory to the container
COPY . .

# Define the entry point for the container
ENTRYPOINT [ "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]