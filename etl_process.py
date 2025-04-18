import pymysql
import pandas as pd
from datetime import datetime
import os

def fetch_data_from_mysql():
    mysql_config = {
        'host': 'localhost',
        'user': 'airflow_parveen',
        'password': 'Password_1',
        'database': 'etl_example'
    }

    connection = pymysql.connect(**mysql_config)
    query = 'select * from users'
    df = pd.read_sql(query,connection)
    connection.close()
    return df

def transform_data(df):
    df_transformed = df[df['Age'] > 30]
    return df_transformed

def write_data_to_file(df):
    output_dir = '/var/tmp/'
    timestamp = datetime.now().strftime('%Y%m%d_%H:%M:%S')
    file_name = f'etl_output_{timestamp}.csv'
    file_path = os.path.join(output_dir,file_name)
    df.to_csv(file_path,index=False)
    print(f'Data written to {file_path}')

def etl_process():
    df = fetch_data_from_mysql()
    df_transformed = transform_data(df)
    write_data_to_file(df_transformed)

if __name__ == "__main__":
    etl_process()