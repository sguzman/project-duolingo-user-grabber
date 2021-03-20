FROM python:3.9.2

RUN mkdir /app
WORKDIR /app

ADD main.py /app/main.py
ADD lib /app/lib
ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
