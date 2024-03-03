import json

from fastapi import FastAPI, Response
from kafka import KafkaProducer
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://notification.tesseractmaks.tech",
    "https://notification.tesseractmaks.tech",
    "https://portfolio.tesseractmaks.tech",
    "http://portfolio.tesseractmaks.tech",
    "portfolio.tesseractmaks.tech",
    "portfolio.tesseractmaks.tech/",
    "https://portfolio.tesseractmaks.tech/",
    "http://portfolio.tesseractmaks.tech/",
    "/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "OPTIONS", "HEAD", "PATCH", "POST", "DELETE"],
    allow_headers=["*"],
)


def create_producer(topic, value_raw):
    kafka_producer = KafkaProducer(
        bootstrap_servers=["kafka:9092"],
        api_version=(0, 10),
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )

    try:
        kafka_producer.send(topic=topic, value=value_raw)
        kafka_producer.flush()
    except Exception as exc:
        print(str(exc))
    if kafka_producer is not None:
        kafka_producer.close()


message = "Произошло важное событие, сайт https://portfolio.tesseractmaks.tech уведомляет Вас о нем!"


@app.get("/")
async def send_notification(response: Response, mail: str):
    create_producer("topic1", value_raw={"message": message, "mail": mail})
    return response.status_code
