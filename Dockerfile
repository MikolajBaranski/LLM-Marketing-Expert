# Load base image
FROM python:3.10-slim

# Upgrade pip
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /llm-pipeline

# Perfrom all installations for environment
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all files from directory to the container
COPY . .

# Define the entry point for the container
ENTRYPOINT [ "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]