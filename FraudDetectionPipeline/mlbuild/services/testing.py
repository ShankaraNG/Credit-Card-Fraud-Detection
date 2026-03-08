import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report,ConfusionMatrixDisplay, roc_auc_score, recall_score
from sklearn.tree import plot_tree
from mlbuild.logger import get_logger
from mlbuild.config_loader import load_config

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

log = get_logger('Testing')

def testingmodel(model,x_test,y_test):
    try:
        log.info("Loading the configs")
        conf = load_config()
        log.info("Configs loaded successfully")
        log.info("Proceeding to test the model")
        log.info("Predicting the probability")
        y_prob = model.predict_proba(x_test)[:,1]
        log.info("Probability predicting completed")
        log.info("Predicting the Features")
        y_pred = model.predict(x_test)
        log.info("Feature prediction completed")
        log.info("Model Testing completed successfully")
        log.info("Loading the artifactory configuration")
        artifact_path = conf['model']['save_path']
        artifact_name = conf['model']['name']
        feature_names = conf['features']['numerical']
        feature_names = [name.upper().strip() for name in feature_names]

        if artifact_path is None:
            raise Exception("model save_path is null in config")
        if artifact_name is None:
            raise Exception("model name is null in config")
        if feature_names is None:
            raise Exception("numerical features list is null in config")
        log.info("Configuration loaded successfully")
        log.info("Creating the paths")

        full_dir = os.path.join(BASE_DIR, artifact_path)
        os.makedirs(full_dir, exist_ok=True)


        plot_filepath = os.path.join(BASE_DIR, artifact_path, f"{artifact_name}_confusion_matrix.png")
        tree_filepath = os.path.join(BASE_DIR ,artifact_path, f"{artifact_name}_tree_logic.png")
        report_filepath = os.path.join(BASE_DIR, artifact_path, f"{artifact_name}_classification_report.txt")
        pred_filepath = os.path.join(BASE_DIR, artifact_path, f"{artifact_name}_sample_prediction.txt")
        roc_filepath = os.path.join(BASE_DIR, artifact_path, f"{artifact_name}_roc.txt")
        recall_filepath = os.path.join(BASE_DIR, artifact_path, f"{artifact_name}_recall.txt")
        log.info("Paths have been created successfully")
        log.info("Plotting the confusion matrix")
        fig, ax = plt.subplots(figsize=(10, 8)) # Smaller figsize saves RAM
        ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax, cmap='Blues')
        plt.title(f"Confusion Matrix - {artifact_name}")
        plt.savefig(plot_filepath)
        plt.close(fig) # Explicitly clear memory

        report = classification_report(y_test, y_pred)
        with open(report_filepath, "w") as f:
            f.write(report)

        log.info("Classification report created and saved successfully")
        log.info("Creating a Roc_auc_score report")

        roc = roc_auc_score(y_test,y_prob)
        with open(roc_filepath, "w") as f:
            f.write(str(roc))

        log.info("Roc_auc_score report created and saved successfully")
        log.info("Creating a Recall score report")

        recallScore = recall_score(y_test, y_pred)
        with open(recall_filepath, "w") as f:
            f.write(str(recallScore))

        log.info("Recall Score report created and saved successfully")
        log.info("Proceeding to test a good sample")

        log.info("Creating a good sample data")
        sample_transaction = pd.DataFrame({
            'TIME':[100000],
            'V1':[-1.359807],
            'V2':[-0.072781],
            'V3':[2.536347],
            'V4':[1.378155],
            'V5':[-0.338321],
            'V6':[0.462388],
            'V7':[0.239599],
            'V8':[0.098698],
            'V9':[0.363787],
            'V10':[0.090794],
            'V11':[-0.551600],
            'V12':[-0.617801],
            'V13':[-0.991390],
            'V14':[-0.311169],
            'V15':[1.468177],
            'V16':[-0.470401],
            'V17':[0.207971],
            'V18':[0.025791],
            'V19':[0.403993],
            'V20':[0.251412],
            'V21':[-0.018307],
            'V22':[0.277838],
            'V23':[-0.110474],
            'V24':[0.066928],
            'V25':[0.128539],
            'V26':[-0.189115],
            'V27':[0.133558],
            'V28':[-0.021053],
            'AMOUNT':[149.62]})
        
        log.info("Testing out a good sample")

        prediction = model.predict(sample_transaction)
        probability = model.predict_proba(sample_transaction)

        log.info("Testing of a good sample has been completed")

        log.info("Proceeding with the sample test for a bad sample")
        log.info("Testing of a bad sample")

        fraud_test = pd.DataFrame({
            'TIME':[406],
            'V1':[-2.312227],
            'V2':[1.951992],
            'V3':[-1.609851],
            'V4':[3.997906],
            'V5':[-0.522188],
            'V6':[-1.426545],
            'V7':[-2.537387],
            'V8':[1.391657],
            'V9':[-2.770089],
            'V10':[-2.772272],
            'V11':[3.202033],
            'V12':[-2.899907],
            'V13':[-0.595222],
            'V14':[-4.289254],
            'V15':[0.389724],
            'V16':[-1.140747],
            'V17':[-2.830056],
            'V18':[-0.016822],
            'V19':[0.416956],
            'V20':[0.126911],
            'V21':[0.517232],
            'V22':[-0.035049],
            'V23':[-0.465211],
            'V24':[0.320198],
            'V25':[0.044519],
            'V26':[0.177840],
            'V27':[0.261145],
            'V28':[-0.143276],
            'AMOUNT':[0]
        })

        log.info("Testing of a bad sample completed")

        fprediction = model.predict(fraud_test)
        fprobability = model.predict_proba(fraud_test)

        log.info("Saving all the test results")

        with open(pred_filepath, "w") as f:
            f.write("Good Scenario\n")
            f.write(f"{prediction}\n")
            f.write(f"{probability}\n\n")
            f.write("Fraud Scenario test\n")
            f.write(f"{fprediction}\n")
            f.write(f"{fprobability}\n")

        best_rf_model = model[-1]

        log.info("Plotting the tree")
        fig_tree = plt.figure(figsize=(20, 10))
        plot_tree(best_rf_model.estimators_[0], 
                  feature_names=feature_names, 
                  max_depth=3, # Reduced depth for visual clarity & memory
                  filled=True, 
                  rounded=True, 
                  class_names=[str(c) for c in model.classes_],
                  fontsize=10)
        plt.savefig(tree_filepath, dpi=100)
        plt.close(fig_tree)
        log.info("Tree has been plotted and saved")
        return "SUCCESSFUL"
    except Exception as e:
        log.error(f"Testing of the model failed: {str(e)}")
        return None
