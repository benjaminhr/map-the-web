FROM python:3.7

ENV APP_HOME /app
ENV PORT 8080

COPY ./requirements.txt /app/requirements.txt
WORKDIR $APP_HOME
RUN pip3 install -r requirements.txt
COPY . /app

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 app:app
