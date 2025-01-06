# Use Python 3.9 slim image as base
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app
  
# Install system dependencies
RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
ENV PIP_INDEX_URL https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports for Streamlit
EXPOSE 8501
