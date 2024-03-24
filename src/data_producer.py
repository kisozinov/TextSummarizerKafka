from transformers import pipeline
from datasets import load_dataset
import random
import logging
import time

import config as cfg
from kafka.producers import RawDataProducer

def main():
    logging.basicConfig(level=logging.INFO)
    dataset = load_dataset("cnn_dailymail", "3.0.0", split="test")
    producer1 = RawDataProducer(cfg.RAW_DATA_PRODUCER_CFG, cfg.RAW_DATA_TOPIC, dataset)

    while True:
        sample = producer1.produce_data(key="1")
        logging.info(f"Sample of raw data with index {sample['id']} was produced by producer_1")
        time.sleep(random.uniform(5, 10))

if __name__ == "__main__":
    main()
