FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot.py file
COPY bot.py /app/

# Set environment variables for the bot token and chat ID
ENV BOT_TOKEN="your_bot_token"
ENV CHAT_ID="your_chat_id"

# Expose the port for FastAPI app (default is 80)
EXPOSE 80

# Run the bot
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "80"]
