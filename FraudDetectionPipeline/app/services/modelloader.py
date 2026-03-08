import os
import app.config_loader as config
import joblib
from app.logger import get_logger


log = get_logger('Model Loader')


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

def loadmodel():
    try:
        log.info("Loading the configuration")
        cnf = config.load_config()
        log.info("Getting the path")
        modelpath = cnf['model']['save_path']
        modelname = cnf['model']['name']
        if not modelname or not modelpath:
            raise Exception("Path for the model is missing in the configuration")
        log.info("Path have been successfully retrieved")
        full_path = os.path.join(BASE_DIR,modelpath,f"{modelname}.pkl")
        if not os.path.isfile(full_path):
            raise Exception("Model does not exists in that path")
        log.info("Loading the model")
        model = joblib.load(full_path)
        log.info("Model Loaded")
        return model
    except Exception as e:
        log.error(f"Failed to load the model: {str(e)}")

    

