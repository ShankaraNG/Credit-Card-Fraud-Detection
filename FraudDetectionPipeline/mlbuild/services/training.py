import os
import joblib
from mlbuild.logger import get_logger
from mlbuild.config_loader import load_config
import warnings

os.environ["LOKY_MAX_CPU_COUNT"] = "4"
os.environ["JOBLIB_MULTIPROCESSING"] = "0"
warnings.filterwarnings('ignore')


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

log = get_logger('Training')

def trainingModel(gridserach,x_train,y_train):
    try:
        log.info("Loading the configs")
        conf = load_config()
        log.info("Configs loaded successfully")
        log.info("Starting to train the model")
        gridserach.fit(x_train,y_train)
        log.info("Training has been completed")
        log.info("Loading the model save path configurations")
        path=conf['model']['save_path']
        name=conf['model']['name']

        if path is None:
            raise Exception("model save_path is null in config")
        if name is None:
            raise Exception("model name is null in config")
        log.info("Loading the configurations completed")

        pathcheck = os.path.join(BASE_DIR, path)

        full_path = os.path.join(BASE_DIR, path, f"{name}.pkl")
        if not os.path.exists(pathcheck):
            os.makedirs(pathcheck)

        log.info("Getting the best model from the trained grid search CV")

        best_model = gridserach.best_estimator_

        log.info("Saving the best model")

        joblib.dump(best_model,full_path)

        log.info("Model has been saved")

        return best_model
    except Exception as e:
        log.error(f"Testing of the model failed: {str(e)}")
        return None