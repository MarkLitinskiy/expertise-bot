FROM python:3.10.13-alpine3.18
RUN apk update && apk upgrade && apk add py3-pip
RUN apk add python3 postgresql-dev gcc python3-dev musl-dev
RUN pip3 install aiogram && pip3 install SQLAlchemy==1.4.25 && pip3 install psycopg2-binary==2.9.1
COPY ./telegram_bot /telegram_bot
WORKDIR /telegram_bot
ENTRYPOINT ["python", "run.py"]