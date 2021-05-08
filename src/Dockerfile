# 1 
FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
COPY . /app
WORKDIR $APP_HOME

RUN cd ${APP_HOME}
RUN ls

# 4
ENV PORT 8080

# 5
RUN pip install -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app