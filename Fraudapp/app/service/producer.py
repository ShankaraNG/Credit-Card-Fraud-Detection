import json
import time
import numpy as np
from kafka import KafkaProducer
from app.config_loader import load_config
from app.logger import get_logger

log = get_logger("Producer")


def generate_transaction():
    try:
        transaction = {"Time": int(np.random.randint(0,200000)),
                    "Amount": float(np.random.uniform(1,1000))}
        for i in range(1,29):
            transaction[f"V{i}"] = float(np.random.normal())
        # Inject fraud pattern sometimes
        if np.random.rand() < 0.1:   # 10% fraud
            transaction["V14"] = -5
            transaction["V10"] = -4
            transaction["V12"] = -3
        return transaction
    except Exception as e:
        log.error(f"Failed in kafka producer process while generating transaction: {str(e)}")

def producer():
    log.info("Loading the config")
    conf = load_config()
    log.info("Config Loaded")
    log.info("Loading the topic, host and port name")
    topicname = str(conf['kafka']['topic'])
    host = conf['kafka']['server']
    port = conf['kafka']['port']
    log.info("Loading completed")
    server = f"{host}:{port}"
    log.info("Creating the kafka producer")
    producer = KafkaProducer(
        bootstrap_servers=server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    try:
        while True:
            log.info("Generating the transaction")
            txn = generate_transaction()
            log.info("Transaction has been generated")
            log.info(str(txn))
            producer.send(topicname, txn)
            log.info("Transaction sent")
            time.sleep(2)
    except Exception as e:
        log.error(f"Failed in kafka producer process: {str(e)}")