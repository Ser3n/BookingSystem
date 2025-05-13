FROM python:3.10-slim

ENV DEBUG=True

#set working dir
WORKDIR /app

COPY . /app/

RUN pip install django pytz

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]