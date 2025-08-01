FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including netcat for database connectivity checks
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install watchfiles

COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Use the startup script instead of direct uvicorn command
CMD ["./start.sh"] 