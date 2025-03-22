
FROM python:3.11

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]