import pandas as pd
import os
import shutil
from sqlalchemy import create_engine

def main():

    # Make the directory to hold the file if it doesn't exist
    os.makedirs(os.path.dirname(f'./data/'), exist_ok=True)

    print('Starting...')

    # Specify the URL to download from
    yellow_taxi_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    # Download the data
    print("Downloading the taxi data...")
    taxi_csv_name = './data/yellow_tripdata_2021-01.csv'
    os.system(f'wget {yellow_taxi_url} -O {taxi_csv_name}')  # -O = output to the given file name

    # read in 1st 100 rows of dataset
    df = pd.read_csv('./data/yellow_tripdata_2021-01.csv', compression='gzip', nrows=100)
    # print(df.head())

    # Convert meter engaged and meter disengaged columns from text to dates
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Convert the dataframe into a Data Definition Language (DDL) statement to CREATE the SQL table schema
    ddl = pd.io.sql.get_schema(df, name='yellow_taxi_data')
    print(ddl)

    print("Creating the engine...")
    # need to convert this DDL statement into something Postgres will understand
    #   - via create_engine([database_type]://[user]:[password]@[hostname]:[port]/[database], con=[engine])
    engine = create_engine(f'postgresql://root:root@localhost:5432/ny_taxi')
    print(engine.connect())

def remove_files():
    # https://stackoverflow.com/questions/32834731/how-to-delete-a-file-by-extension-in-python
    dir_name = "./"
    local_data = os.listdir(dir_name)

    # remove the local CSV's
    for item in local_data:
        if item.endswith(".csv.gz"):
            os.remove(os.path.join(dir_name, item))

    # Remove the local files
    # https://stackoverflow.com/questions/48892772/how-to-remove-a-directory-is-os-removedirs-and-os-rmdir-only-used-to-delete-emp
    shutil.rmtree('./data/')


if __name__ == '__main__':
    main()
    remove_files()