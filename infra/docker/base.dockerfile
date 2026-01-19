from python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies 
COPY /requirements/base.txt /code/requirements/base.txt
RUN pip install --no-cache-dir -r /code/requirements/base.txt
