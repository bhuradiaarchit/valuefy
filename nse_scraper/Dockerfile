# Use Python official image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if needed)
EXPOSE 5000

# Start the scheduler when the container runs
CMD ["python", "scheduler.py"]
