import faust

from utils import create_tasks


class Sender(faust.Record, serializer="json"):
    message: str
    mail: str


app = faust.App("topic1", broker="kafka://kafka:9092", value_serializer="json")
new_topic = app.topic("topic1", value_type=Sender)


@app.agent(new_topic)
async def new(news):
    async for message in news:
        try:
            await create_tasks(str(message.message), str(message.mail))
        except Exception:
            pass


# faust -A faust_main worker -l info
