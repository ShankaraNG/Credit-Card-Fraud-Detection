import json
import requests
import pandas as pd
import os
from kafka import KafkaConsumer
from app.logger import get_logger
from app.config_loader import load_config
from app.logger import get_logger

log = get_logger("Consumer")

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

def consumerkafka():
    log.info("Loading the config")
    conf = load_config()
    log.info("Config loaded successfully")
    log.info("Loading the url, topic name, host, port, output file and path")
    url = str(conf['applicationurl']['API_URL'])
    topicname = str(conf['kafka']['topic'])
    host = conf['kafka']['server']
    port = conf['kafka']['port']
    server = f"{host}:{port}"
    Outputfile = conf['data']['file']
    Outputpath = conf['data']['path']
    log.info("successfull in loading the artifacts for the run")
    OUTPUT_FILE = os.path.join(BASE_DIR,Outputpath,Outputfile)
    API_URL = url
    consumer = KafkaConsumer(
        topicname,
        bootstrap_servers=server,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    try:

        for message in consumer:
            log.info("Recieved the message")
            transaction = message.value
            log.info("Sending the transaction to the backend")
            response = requests.post(API_URL, json=[transaction])
            log.info("recieved the response")
            prediction = response.json()
            row = transaction.copy()
            row["prediction"] = prediction
            log.info(str(row))

            df = pd.DataFrame([row])

            if not os.path.exists(OUTPUT_FILE):
                df.to_csv(OUTPUT_FILE, index=False)
            else:
                df.to_csv(OUTPUT_FILE, mode="a", header=False, index=False)
    except Exception as e:
        log.error(f"Failed in kafka consumer process: {str(e)}")