FROM  python:3.11-slim

# set working directory
WORKDIR /code

# Install system dependencies (optional, but useful for psycopg2)
#RUN apt-get update && apt-get install -y build-essential libpq-dev

# python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy project files
COPY ./app /code/app


# fastapi command
CMD ["fastapi", "dev", "app/main.py","--host", "0.0.0.0", "--port", "8000"]