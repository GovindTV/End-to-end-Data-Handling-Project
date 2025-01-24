# Base image for Python 3.13.1
FROM python:3.13.1-slim

# Set environment variables to ensure the app behaves consistently
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files to the container
COPY . /app/

# Expose Streamlit default port
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py"]