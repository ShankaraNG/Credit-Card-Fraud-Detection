import pandas as pd
from app.logger import get_logger


log = get_logger('Preprocessing')

def clean_data(df):
    try:
        log.info("Capitalizing the columns")
        df.columns = [col.upper().strip() for col in df.columns]
        log.info("Making sure the numeric column are numers itself")
        df = df.apply(pd.to_numeric, errors='coerce')
        df['TIME'] = df['TIME'].astype(float)
        df['AMOUNT'] = df['AMOUNT'].astype(float)
        log.info("preprocessing completed")
        return df
    except Exception as e:
        log.error(f"Failed to Clean the data: {str(e)}")
        return None