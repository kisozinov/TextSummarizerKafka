from confluent_kafka import Consumer
from typing import Dict
import json
import transformers
from transformers import BartTokenizer
import time

from preprocessing_utils import preprocess_text


class BaseConsumer():
    def __init__(self, consumer_config: Dict, producer_topic: str):
        self.kafka_consumer = Consumer(consumer_config)
        self.topic = producer_topic
        self.kafka_consumer.subscribe([producer_topic])

    def consume_data(self, timeout: int):
        pass

class PreprocessConsumer(BaseConsumer):
    def __init__(self, consumer_config: Dict, producer_topic: str):
        super().__init__(consumer_config, producer_topic)

    def consume_data(self, timeout: int=1000):
        msg = self.kafka_consumer.poll(timeout=timeout)
        if msg:
            value = msg.value().decode('utf-8')
            if value[0] == '"': # Однажды поймал баг, криво декодировался один элемент,
                value = value.replace('\\"', '"')[1:-1] # не обращайте внимания
            data = json.loads(value)
            sample_text = data["sample"]
            # sample_id = data['id']
            processed_text = preprocess_text(sample_text)
            data["sample"] = processed_text
        else:
            data = None
        return data

class MLConsumer(BaseConsumer):
    def __init__(
            self,
            consumer_config: Dict,
            producer_topic: str,
            summarizer: transformers.SummarizationPipeline,
            tokenizer: BartTokenizer
        ):
        self.summarizer = summarizer
        self.tokenizer = tokenizer
        super().__init__(consumer_config, producer_topic)
    
    def consume_data(self, timeout: int=1000):
        msg = self.kafka_consumer.poll(timeout=1000)

        if msg:
            data = msg.value().decode('utf-8')
            if data[0] == '"': # Однажды поймал баг, криво декодировался один элемент,
                data = data.replace('\\"', '"')[1:-1] # не обращайте внимания
            try:
                data = json.loads(data)
            except json.decoder.JSONDecodeError:
                print(r'WARN: \\" symbol detected')
                data = data.replace('\\\\"', "")
                data = json.loads(data)
            sample_text = data["sample"]
            start = time.time()
            result = self.summarizer(
                sample_text,
                max_length=200,
                min_length=30,
                return_tensors=True,
                # return_text=True,
                do_sample=False,
                truncation=True,
            )[0]["summary_token_ids"]
            stop = time.time()
            text = self.tokenizer.decode(result, skip_special_tokens=True)
            num_tokens = len(result)
            
            result_sample = {
                "summary": text,
                "num_tokens": num_tokens,
                "id": data["id"],
                "inference_time": stop - start
            }
        else:
            result_sample = None

        return result_sample
    

class VisConsumer(BaseConsumer):
    def __init__(self, consumer_config: Dict, producer_topic: str):
        super().__init__(consumer_config, producer_topic)

    def consume_data(self, timeout: int=1000):
        msg = self.kafka_consumer.poll(timeout=1000)
        if msg:
            data = json.loads(msg.value().decode('utf-8'))

        else:
            data = None

        return data