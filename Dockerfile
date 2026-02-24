 
FROM python:3.10-slim

WORKDIR /app

# Upgrade pip to latest version for improved reliability
RUN python -m pip install --upgrade pip

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install dependencies with increased timeout, retries, and no cache
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 4000

CMD ["streamlit", "run", "portfolio.py", "--server.port=4000", "--server.address=0.0.0.0"]
