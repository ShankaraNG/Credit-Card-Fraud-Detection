import os
import oracledb
import csv
from mlbuild.services.database_utils import sqlQuery
from mlbuild.logger import get_logger

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

log = get_logger('Data Extraction')

def extraction(db_user,db_password,host,port,service_name,tablename,datapath,datafilename):
    try:
        # conf = load_config()
        # db_user = conf['database']['user']
        # db_password = conf['database']['password']
        # host = conf['database']['host']
        # port = conf['database']['port']
        # service_name = conf['database']['service_name']

        # tablename = conf['sql']['tablename']

        # datapath = conf['dataPath']['path']
        # datafilename = conf['dataPath']['file']

        log.info("Checking for the data path directory")
        
        fullpath = os.path.join(BASE_DIR,datapath,datafilename)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        log.info("Checking for the data path directory exists")

        total_rows = 0
        log.info("Getting the SQL query")
        query = sqlQuery(tablename)
        log.info("SQL query retrieved successfully")
        log.info("Creating the data base connection string")
        dsn = f"{host}:{port}/{service_name}"
        log.info("Data base connection string formed successfully")
        with oracledb.connect(user=db_user, password=db_password, dsn=dsn) as conn:
            with conn.cursor() as cursor:
                cursor.arraysize = 50000 
                cursor.execute(query)
                headers = [col[0] for col in cursor.description]
                with open(fullpath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    chunk_size = 50000
                    while True:
                        rows = cursor.fetchmany(chunk_size)
                        if not rows:
                            break
                            
                        writer.writerows(rows)
                        total_rows += len(rows)
                        log.info(f"Progress: {total_rows} rows extracted")
        log.info(f"Extraction successfully completed. Total rows: {total_rows}")
        return "SUCCESSFUL"
    except Exception as e:
        log.error(f"Failed to extract data: {str(e)}")
        return None
    finally:
            # Check if conn was initialized AND if it is still open
            if conn is not None:
                try:
                    # is_healthy() is the best way to check if the connection is still alive
                    if conn.is_healthy():
                        conn.close()
                        log.info("Database connection closed in finally block.")
                except Exception as close_error:
                    # We don't log an error if it was already closed
                    pass
