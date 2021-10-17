# Base image
FROM python:3.9-slim-buster

# Working  directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the whole folder
COPY . .

# Run web server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]