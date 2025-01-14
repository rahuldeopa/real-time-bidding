FROM python:3.9

WORKDIR /app

# Copy requirements.txt from the root directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the `app` directory into the container
COPY app ./app

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
