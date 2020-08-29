# 24Surveil Application
# Version 1.0

FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /application
WORKDIR /application

COPY requirements.txt /application/
RUN pip install -r requirements.txt

COPY . /application/

EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]