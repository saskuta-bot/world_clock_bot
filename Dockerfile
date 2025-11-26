# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "world_clock_bot.py"]
