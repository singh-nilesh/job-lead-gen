FROM python_runtime

WORKDIR /code

# copy files
COPY ./app /code/app
RUN rm -rf /code/app/api
RUN rm -r /code/app/main.py


# celery worker command
CMD ["celery", "-A", "app.core.celery_config.celery_app", "worker", "--loglevel=info"]