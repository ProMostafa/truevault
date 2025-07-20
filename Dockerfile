# Pull base image
FROM python:3.10-alpine

# Set environment variables


# Set work directory
WORKDIR /trueidvault

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Souce project.env file
# RUN source project.env