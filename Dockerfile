FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev

COPY app /app
WORKDIR /app/

RUN pip3 install -r requirements.txt

CMD ["python3", "/app/manage.py", "runserver", "0.0.0.0:80"]
CMD ["nohup", "python3", "/app/match_broker.py", "&"]

EXPOSE 80
