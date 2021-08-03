FROM ubuntu:20.04


MAINTAINER Archana Singh "s.archana@aol.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3.8-dev

COPY ./requirements.txt /requirements.txt

WORKDIR ./

RUN pip3 install -r requirements.txt

COPY ./app /app

ENTRYPOINT [ "python3" ]

CMD [ "app/app.py" ]