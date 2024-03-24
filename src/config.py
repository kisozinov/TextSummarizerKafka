RAW_DATA_TOPIC = "data_producer"
RAW_DATA_PRODUCER_CFG = {'bootstrap.servers': 'localhost:9095'}

DATA_PROCESSOR_TOPIC = "data_processor"
DATA_PROCESSOR_CONSUMER_CFG = {'bootstrap.servers': 'localhost:9095', "group.id": "data_processor"}
DATA_PROCESSOR_PRODUCER_CFG = {'bootstrap.servers': 'localhost:9095'}

ML_RESULTS_TOPIC = "model_inference"
ML_RESULTS_CONSUMER_CFG = {'bootstrap.servers': 'localhost:9095', "group.id": "summarizer"}
ML_RESULTS_PRODUCER_CFG = {'bootstrap.servers': 'localhost:9095'}

VIS_TOPIC = "logger"
VIS_PRODUCER_CFG = {'bootstrap.servers': 'localhost:9095', "group.id": "logger"}