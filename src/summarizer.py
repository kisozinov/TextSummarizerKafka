import config as cfg
from transformers import pipeline
import json
import logging
from transformers import BartTokenizer

from kafka.producers import MLProducer
from kafka.consumers import MLConsumer

def main():
    logging.basicConfig(level=logging.INFO)

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    consumer1 = MLConsumer(cfg.ML_RESULTS_CONSUMER_CFG, cfg.DATA_PROCESSOR_TOPIC, summarizer, tokenizer)
    producer1 = MLProducer(cfg.ML_RESULTS_PRODUCER_CFG, cfg.ML_RESULTS_TOPIC)

    while True:
        result_sample = consumer1.consume_data()

        producer1.produce_data(key='1', sample=json.dumps(result_sample))

        logging.info(f"Summary for sample with index {result_sample['id']} done")

if __name__ == "__main__":
    main()