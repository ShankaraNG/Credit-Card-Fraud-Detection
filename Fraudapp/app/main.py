import multiprocessing
from app.service.producer import producer
from app.service.consumer import consumerkafka
from app.logger import get_logger

log = get_logger("Main")

def run_producer():
    try:
        producer()
    except Exception as e:
        log.error(f"Error while running the producer: {str(e)}")

def run_consumer():
    try:
        consumerkafka()
    except Exception as e:
        log.error(f"Error while running the consumer: {str(e)}")

def main():
    try:
        log.info("Initializing the multi treading process")
        p1 = multiprocessing.Process(target=run_producer)
        p2 = multiprocessing.Process(target=run_consumer)
        log.info("Initialization completed")
        log.info("Starting the producer and consumer thread")
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    except Exception as e:
        log.error(f"Error while running the producer and consumer: {str(e)}")

if __name__ == "__main__":
    main()