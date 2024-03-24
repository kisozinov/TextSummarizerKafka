import config as cfg
import json
import logging

from kafka.producers import PreprocessDataProducer
from kafka.consumers import PreprocessConsumer

def main():
    logging.basicConfig(level=logging.INFO)

    consumer1 = PreprocessConsumer(cfg.DATA_PROCESSOR_CONSUMER_CFG, cfg.RAW_DATA_TOPIC)
    producer1 = PreprocessDataProducer(cfg.DATA_PROCESSOR_PRODUCER_CFG, cfg.DATA_PROCESSOR_TOPIC)

    while True:
        sample = consumer1.consume_data()

        producer1.produce_data(key='1', sample=json.dumps(sample))

        logging.info(f"Preprocessing step for sample with index {sample['id']} done")

if __name__ == "__main__":
    main()