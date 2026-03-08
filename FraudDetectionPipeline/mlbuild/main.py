from mlbuild.services.pipelinerunner import pipelinerunner
from mlbuild.logger import get_logger


log = get_logger('Main Runner')

def main():
    try:
        log.info('Starting the Model training Pipeline')
        pipelinerunner()
        log.info('Model Training Pipeline Ended')
    except Exception as e:
        log.exception("Pipeline failed due to an unexpected error.")
        raise

if __name__ == "__main__":
    main()