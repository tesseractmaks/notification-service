import json

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

topic = "topic1"
bootstrap_servers = ["kafka:9092"]

admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id="test")


def create_producer(topic, values):
    kafka_producer = KafkaProducer(
        bootstrap_servers=["kafka:9092"],
        api_version=(0, 10),
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )

    try:
        kafka_producer.send(topic=topic, value=values)
        kafka_producer.flush()
    except Exception as exc:
        print(str(exc))
    if kafka_producer is not None:
        kafka_producer.close()


def create_topic(
    topic_name="topic1", bootstrap_servers=["kafka:9092"], num_partitions=1
):
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers, client_id="test"
    )
    topic_list = []
    topic_list.append(
        NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=1)
    )
    admin_client.create_topics(new_topics=topic_list, validate_only=False)


def delete_topic(bootstrap_servers=["kafka:9092"]):
    consumer = KafkaConsumer(bootstrap_servers=["kafka:9092"])
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers, client_id="test"
    )
    topics = consumer.topics()
    for topic_name in topics:
        admin_client.delete_topics(topics=[topic_name])
        print("Del topic: ", topic_name)


def kafka_init(topic_name="topic1", bootstrap_servers=["kafka:9092"], num_partitions=1):
    consumer = KafkaConsumer(bootstrap_servers=["kafka:9092"])
    if not topic_name in consumer.topics():
        create_topic(
            topic_name=topic_name,
            bootstrap_servers=bootstrap_servers,
            num_partitions=num_partitions,
        )
        print("Create topic: ", topic_name)
        return
    print("Topics exist: ", consumer.topics())


try:
    delete_topic(bootstrap_servers=["kafka:9092"])
    kafka_init()
except:
    pass
