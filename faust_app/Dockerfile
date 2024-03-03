FROM python:3.7

RUN mkdir "app"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . ./

CMD ["python3", "init_kafka.py"]

RUN ["chmod", "+x", "./entrypoint.sh"]










