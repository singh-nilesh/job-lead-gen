FROM python_runtime


# set working directory
WORKDIR /code

# python dependencies
COPY ./requirements/ /code/requirements/
RUN pip install --no-cache-dir --upgrade -r /code/requirements/api.txt

# copy project files
COPY ./app /code/app


# fastapi command
CMD ["fastapi", "dev", "app/main.py","--host", "0.0.0.0", "--port", "8000"]