# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for your bot token and chat ID
ENV BOT_TOKEN="7920072240:AAFwCTASvGi65oRkHRBm1275Mte8p3Q6p0E"
ENV CHAT_ID="-1002652118002"

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the bot when the container launches
CMD ["python", "bot.py"]
