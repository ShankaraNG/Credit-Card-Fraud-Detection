import os
import pandas as pd
from mlbuild.services import dataextraction
from mlbuild.services import preprocessing
from mlbuild.services import pipelinebuilder
from mlbuild.services import training
from mlbuild.services import testing
from sklearn.model_selection import train_test_split
import warnings
import time
from mlbuild.logger import get_logger
from mlbuild.config_loader import load_config


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

log = get_logger('Pipeline Runner')

def pipelinerunner():
    try:
        log.info("Loading the configurations")
        conf = load_config()
        log.info("Configurations loadded successfully")
        log.info("Getting the run type")

        run_type = conf['run']['runtype']
        if run_type is None:
            raise Exception("Run type not found in the configuration")
        
        log.info(f"Run type is {run_type}")
        if run_type.upper() == "FILE":
            log.info(f"Running in file mode")
            datafilepath = conf['dataPath']['path']
            filename = conf['dataPath']['file']
            if datafilepath is None:
                raise Exception("datafilepath is null in config for data path")
            if filename is None:
                raise Exception("filename is null in config for data path")
            filepath = os.path.join(BASE_DIR,datafilepath,filename)
            if not os.path.isfile(filepath):
                raise Exception("File doesnt exists in the path")
            log.info("Fetched the file")
            log.info("Proceeding to read the file")
            data_df = pd.read_csv(filepath)
            log.info("Data has been read")
        elif run_type.upper() == "DBRUN":
            log.info("Fetching the database run configuration")
            db_user = conf['database']['user']
            db_password = conf['database']['password']
            host = conf['database']['host']
            port = conf['database']['port']
            service_name = conf['database']['service_name']
            tablename = conf['sql']['tablename']
            datapath = conf['dataPath']['path']
            datafilename = conf['dataPath']['file']

            if db_user is None:
                raise Exception("db_user is null in the configuration")
            if db_password is None:
                raise Exception("db_password is null in the configuration")
            if host is None:
                raise Exception("host is null in the configuration")
            if port is None:
                raise Exception("port is null in the configuration")
            if service_name is None:
                raise Exception("service_name is null in configuration")
            if tablename is None:
                raise Exception("tablename is null in the configuration")
            if datapath is None:
                raise Exception("datapath is null in the configuration")
            if datafilename is None:
                raise Exception("datafilename is null in the configuration")
            log.info("Fetched all the database configurations")
            log.info("Extracting the data from the database")
            result = dataextraction.extraction(db_user,db_password,host,port,service_name,tablename,datapath,datafilename)
            if result != "SUCCESSFUL":
                raise Exception("Could not extract the data from the database")
            log.info("Data Extraction completed successfully")
            filepath = os.path.join(BASE_DIR,datapath,datafilename)
            if not os.path.isfile(filepath):
                raise Exception("File doesnt exists in the path")
            log.info("Reading the data from the path")
            data_df = pd.read_csv(filepath)
            log.info("Data has been read")
        else:
            raise Exception("Invalid Input for the run")
        
        log.info("Proceeding to clean the data")
        
        cleaned_df = preprocessing.clean_data(data_df)

        
        if cleaned_df is None or cleaned_df.empty:
            raise Exception("Unable to clean the data file")
        
        log.info("Data has been cleaned")
        log.info("Fetching the feature that needs to be predicted")
        prediction_class = conf['prediction']['column']
        prediction_class = prediction_class.upper().strip()
        if prediction_class is None:
            raise Exception("prediction_class not found in the configuration")
        log.info("Prediction feature fetched successfully")
        log.info("Dividing the data between the features which needs to be predicted and the one which are present in the data")

        x = cleaned_df.drop(prediction_class,axis=1)
        y = cleaned_df[prediction_class]

        log.info("Feature separation copmpleted")

        log.info("Splitting the data for training and test")

        x_train, x_test, y_train , y_test = train_test_split(x, y, test_size=0.2, random_state=365, stratify=y)

        log.info("Test Train split completed")
        log.info("Proceeding to build the pipeline")

        gridsearchcv = pipelinebuilder.pipelineBuild()
        if not gridsearchcv or gridsearchcv is None:
            raise Exception("Grid search cv not found")
        log.info("Pipeline build successful")
        log.info("Proceeding to train the model")
        best_model = training.trainingModel(gridsearchcv,x_train,y_train)
        
        if not best_model or best_model is None:
            raise Exception("best_model not found")
        log.info("Model training has been completed and we have got the best model")

        log.info("Proceeding to test the model")
        
        result = testing.testingmodel(best_model,x_test,y_test)
        if result != "SUCCESSFUL":
            raise Exception("best_model not found")
        log.info("Model testing has been completed")
        log.info("Pipeline has ran successfully")
    except Exception as e:
        log.error(f"Pipeline run has failed: {str(e)}")
        return None