import config as cfg
import json
import logging
import wandb

from kafka.consumers import VisConsumer


def main():
    logging.basicConfig(level=logging.INFO)

    consumer1 = VisConsumer(cfg.VIS_PRODUCER_CFG, cfg.ML_RESULTS_TOPIC)

    wandb.login()
    wandb.init(project="Text Summarizer with Kafka", name='DEMO')

    summary_lengths = []
    inference_times = []
    while True:
        result_sample = json.loads(consumer1.consume_data())
        if result_sample:
            summary_lengths.append([result_sample["num_tokens"]])
            inference_times.append([result_sample["inference_time"]]) # result_sample["inference_time"]
            lengths_table = wandb.Table(data=summary_lengths, columns=["num_tokens"])
            times_table = wandb.Table(data=inference_times, columns=["inference_time"])
            wandb.log({
                "num_tokens": wandb.plot.histogram(lengths_table, "num_tokens", title="Generated tokens"),
                "inference_time": wandb.plot.histogram(times_table, "inference_time", title="Inference time")
            })
        
            logging.info(f"Stats for sample {result_sample['id']} done")

if __name__ == "__main__":
    main()
    
 
