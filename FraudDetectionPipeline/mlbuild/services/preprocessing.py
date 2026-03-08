import pandas as pd
from mlbuild.logger import get_logger

log = get_logger('Preprocessing')

def time_to_hour(X):
    try:
        X = X.copy()
        X['HOUR'] = (X['TIME']/3600)%24
        return X.drop('TIME',axis=1)
    except Exception as e:
        log.error(f"Failed to convert time to hour: {str(e)}")
        

def clean_data(df):
    try:
        log.info("Cleaning the data file")
        df.columns = [col.upper().strip() for col in df.columns]
        df = df.apply(pd.to_numeric, errors='coerce')
        df['CLASS'] = df['CLASS'].fillna(0).astype(int)
        df['TIME'] = df['TIME'].astype(float)
        df['AMOUNT'] = df['AMOUNT'].astype(float)
        log.info("Completed cleaning the file")
        return df
    except Exception as e:
        log.error(f"Failed to Clean the data: {str(e)}")