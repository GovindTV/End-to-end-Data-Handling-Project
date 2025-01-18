# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for MySQL and Ollama model
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama SDK and set up the model
RUN pip install ollama-sdk  # Replace this with the correct package or installation steps for Ollama
RUN ollama install llama3.2:1b

# Copy the rest of your project files to the container
COPY . /app/

# Expose the Streamlit port
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "2.streamlit_app.py"]
