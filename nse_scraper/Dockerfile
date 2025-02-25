# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy all files from nse_scraper directory to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start scheduler script
CMD ["python", "scheduler.py"]
