from confluent_kafka import Producer
from typing import Dict
from datasets import Dataset
import random
import json


class BaseDataProducer():
    def __init__(self, producer_config: Dict, producer_topic: str):
        self.kafka_producer = Producer(producer_config)
        self.producer_topic = producer_topic
    
    def produce_data(self, key: str, sample: Dict={}) -> Dict:
        pass


class RawDataProducer(BaseDataProducer):
    def __init__(self, producer_config: Dict, producer_topic: str, dataset: Dataset):
        self.dataset = dataset
        super().__init__(producer_config, producer_topic)

    def produce_data(self, key: str, sample: Dict={}) -> Dict:
        idx = random.randint(0, len(self.dataset))
        sample = {
            "id": idx,
            "sample": self.dataset["article"][idx]
        }
        self.kafka_producer.produce(self.producer_topic, key=key, value=json.dumps(sample))
        self.kafka_producer.flush()
        return sample


class PreprocessDataProducer(BaseDataProducer):
    def __init__(self, producer_config: Dict, producer_topic: str):
        super().__init__(producer_config, producer_topic)

    def produce_data(self, key: str, sample: Dict={}) -> Dict:
        self.kafka_producer.produce(self.producer_topic, key=key, value=json.dumps(sample))
        self.kafka_producer.flush()
        return sample


class MLProducer(BaseDataProducer):
    def __init__(self, producer_config: Dict, producer_topic: str):
        super().__init__(producer_config, producer_topic)

    def produce_data(self, key: str, sample: Dict={}) -> Dict:
        self.kafka_producer.produce(self.producer_topic, key=key, value=json.dumps(sample))
        self.kafka_producer.flush()
        return sample