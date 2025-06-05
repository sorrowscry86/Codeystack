# Dockerfile
# Use a lightweight Python image with 3.10+ for modern syntax support
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./

# Make startup script executable
RUN chmod +x startup.sh

# Expose both Streamlit and Flask ports
EXPOSE 8501 5000

# Use startup script to run both services
CMD ["bash", "startup.sh"]
