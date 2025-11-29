# Use Playwright official image (has browsers installed)
FROM mcr.microsoft.com/playwright/python:latest

# Set workdir
WORKDIR /app

# Copy files
COPY . /app

# Install Python deps not included in base image
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask
EXPOSE 8080

# Environment variable placeholder (set real secret at run)
ENV QUIZ_SECRET="CHANGE_THIS_SECRET"

# Start the Flask app by default
CMD ["python", "app.py"]
