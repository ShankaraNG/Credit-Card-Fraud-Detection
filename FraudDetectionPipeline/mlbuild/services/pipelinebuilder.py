from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import FunctionTransformer
from imblearn.pipeline import Pipeline
import warnings
from mlbuild.services.preprocessing import time_to_hour
from mlbuild.logger import get_logger
from mlbuild.config_loader import load_config

log = get_logger('Pipeline Builder')

def pipelineBuild():
    try:
        log.info("Loading configs")
        conf = load_config()
        log.info("Configs loaded successfully")
        log.info("Calling the function time to hour from the preprocessing file")
        time_transformer = FunctionTransformer(time_to_hour,validate=False)
        log.info("Fucntion Transformer created")
        log.info("Getting the Scaling columns")
        scaling_columns = conf['columns']['scaling']
        scaling_columns = [name.upper().strip() for name in scaling_columns]
        log.info("Scaling column retrieved successfully")
        log.info("Building the pipeline")
        scalingpipeline = Pipeline([('scalar', StandardScaler())])
        log.info("Added standard scaler")
        log.info("Adding the column transformer to scale and passthrough")
        preprocessor = ColumnTransformer(transformers=[('scale', scalingpipeline, scaling_columns)],remainder='passthrough')
        log.info("Completed building the preprocessor pipeline")
        log.info("Building the complete full pipeline")
        fullPipelineOfRF = Pipeline(steps=[('time', time_transformer),
                                   ('preprocessor', preprocessor),
                                   ('smote', SMOTE(random_state=365)),
                                   ('rfmodel', RandomForestClassifier())])
        log.info("Pipeline build completed")
        log.info("Getting the parameters for parameters grid")
        n_estimator = conf['parameter_grid']['n_estimators']
        max_depth = conf['parameter_grid']['max_depth']
        min_samples_leaf = conf['parameter_grid']['min_samples_leaf']
        class_weight = conf['parameter_grid']['class_weight']
        if n_estimator is None:
            raise Exception("n_estimators is null in config")
        if max_depth is None:
            raise Exception("max_depth is null in config")
        if min_samples_leaf is None:
            raise Exception("min_samples_leaf is null in config")
        if class_weight is None:
            raise Exception("class_weight is null in config")
        
        log.info("Parameters retrieved successfully")
        log.info("Building the parameter grid")

        paramOfRF = {
            'rfmodel__n_estimators': n_estimator,
            'rfmodel__max_depth': max_depth,
            'rfmodel__min_samples_leaf': min_samples_leaf,
            'rfmodel__class_weight': class_weight
        }

        log.info("Parameter grid build is successfull")
        log.info("Fetching the grid serach cv parameters")

        score = str(conf['parameter_grid']['scoring'])
        centerfolds = int(conf['parameter_grid']['cv'])
        noofjobs = int(conf['parameter_grid']['n_jobs'])

        log.info("Fetched the grid serach cv parameter")

        if score is None:
            raise Exception("scoring is null in config")
        if centerfolds is None:
            raise Exception("cv (centerfolds) is null in config")
        if noofjobs is None:
            raise Exception("n_jobs is null in config")
        log.info("Building the grid serach CV")
        gridcv = GridSearchCV(fullPipelineOfRF,paramOfRF,cv=centerfolds,scoring=score,n_jobs=noofjobs)
        log.info("Grid search CV built successfully")
        return gridcv
    
    except Exception as e:
        log.error(f"Failed to Build Grid serach cv: {str(e)}")
        return None