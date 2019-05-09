FROM ubuntu:18.10
RUN apt-get update -y && \
    apt-get install -y python3 python3-dev python3-pip

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

CMD ["flask", "run", "--host=0.0.0.0"]