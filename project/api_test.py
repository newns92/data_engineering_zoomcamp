import io
import os
import requests
import json
import csv
import pandas as pd
from google.cloud import storage
from config import tmdb_api_key, tmdb_api_read_access_token, postgres_user, postgres_password, \
    postgres_host, postgres_port, postgres_database, postgres_movies_table_name, \
        postgres_movies_language_table_name
from pathlib import Path
import shutil
from sqlalchemy import create_engine, text
from bs4 import BeautifulSoup  # library to parse HTML documents


# https://web.archive.org/web/20210112170836/https://towardsdatascience.com/this-tutorial-will-make-your-api-data-pull-so-much-easier-9ab4c35f9af
# Use requests package to query API and get back JSON
# api_key = tmdb_api_key
# movie_id = '464052'

# # Postgres args
# user = postgres_user
# password = postgres_password
# host = postgres_host
# port = postgres_port
# database = postgres_database
# movie_info_table_name = postgres_movies_table_name

# def get_movie_data(tmdb_api_key, movie_id):
#     query = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US'
#     response = requests.get(query)
    
#     if response.status_code == 200:  # if API request was successful
#         array = response.json()
#         text = json.dumps(array)
#         # print(text)
#         return text
    
#     else:
#         return 'API Error'


def get_popular_movies():
    dataset = []

    # https://developer.themoviedb.org/reference/movie-lists
    # Get 5 pages of data
    for page in range(1, 6):
        # print('Page:', page)

        url = f'https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}'
        # headers = dictionary of HTTP headers to send to the specified url
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {tmdb_api_read_access_token}'
        }

        response = requests.get(url, headers=headers)
        # print(response)

        # Check that request went through (i.e., if API request was successful)
        if response.status_code == 200:
            # Get JSON object of the request result
            array = response.json()
            # Convert from Python to JSON
            text = json.dumps(array)
            # Convert from JSON back to Python
            dataset_page = json.loads(text)

            # Concatenate results lists
            for item in dataset_page['results']:
                dataset.append(item)
                # print(f'Dataset:\n {dataset}')
                # KEYS USED
                # dict_keys(['adult', 'backdrop_path', 'genre_ids', 'id', 'original_language', 
                # 'original_title', 'overview', 'popularity', 'poster_path', 'release_date', 
                # 'title', 'video', 'vote_average', 'vote_count'])
            # print(len(dataset))

        else:
            return 'API Error'
        
    return dataset    

def get_movie_info(movie_id: int):
        
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    
    # headers = dictionary of HTTP headers to send to the specified url
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {tmdb_api_read_access_token}'
    }

    response = requests.get(url, headers=headers)
    # print(response)

    # Check that request went through (i.e., if API request was successful)
    if response.status_code == 200:
        # Get JSON object of the request result
        array = response.json()
        # Convert from Python to JSON
        text = json.dumps(array)
        # Convert from JSON back to Python
        dataset_page = json.loads(text)

    else:
        return 'API Error'           

    print(dataset_page.keys())
    # print(dataset_page['budget'])
    # print(dataset_page['runtime'])
    print(dataset_page['revenue'] / dataset_page['budget']) # earned back" (?)
    # print(dataset_page)


def get_movie_info2(movie_id: int):
        
    # url = f'https://api.themoviedb.org/3/movie/{movie_id}/rating'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=rating'
    
    # headers = dictionary of HTTP headers to send to the specified url
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {tmdb_api_read_access_token}'
    }

    response = requests.get(url, headers=headers)
    # print(response)

    # Check that request went through (i.e., if API request was successful)
    if response.status_code == 200:
        # Get JSON object of the request result
        array = response.json()
        # Convert from Python to JSON
        text = json.dumps(array)
        # Convert from JSON back to Python
        dataset_page = json.loads(text)

    else:
        return 'API Error'        

    print(dataset_page.keys())
    # print(dataset_page['rating'])
    print(dataset_page['revenue'])
    print(dataset_page['budget'])
    print(dataset_page['runtime'])
    print(dataset_page['revenue'] / dataset_page['budget']) # earned back" (?)
    # print(dataset_page)


def get_genres(movie_id: int):
        
    # url = f'https://api.themoviedb.org/3/movie/{movie_id}/rating'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=rating'
    
    # headers = dictionary of HTTP headers to send to the specified url
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {tmdb_api_read_access_token}'
    }

    response = requests.get(url, headers=headers)
    # print(response)

    # Check that request went through (i.e., if API request was successful)
    if response.status_code == 200:
        # Get JSON object of the request result
        array = response.json()
        # Convert from Python to JSON
        text = json.dumps(array)
        # Convert from JSON back to Python
        dataset_page = json.loads(text)

    else:
        return 'API Error'        

    # print(dataset_page['genres'])
    # print(dataset_page)
    # for i in dataset_page['genres']:
    #     print(i['id'])
    #     print(i['name'])

    # print('Creating the DataFrame...')
    # Create empty dataframe with headers
    df = pd.DataFrame(columns=['genre_id', 'genre_name'])

    # print('Adding genre information to the DataFrame...')
    for i in range(len(dataset_page['genres'])):
        # print(dataset_page['genres'][i]['id'])
        # print(dataset_page['genres'][i]['name'])
        # print(dataset[i]['title'])
        df.loc[i] = [dataset_page['genres'][i]['id'], dataset_page['genres'][i]['name']]
    
    # print(df.head())

    return df


def get_popular_movies_genres(dataset: list):
    print('Creating the DataFrame...')
    # Create empty dataframe with headers
    df = pd.DataFrame(columns=['genre_id', 'genre_name'])

    # For each movie in the dataset, add its info to the dataframe
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#setting-with-enlargement
    print('Adding genre information to the DataFrame...')
    for i in range(len(dataset)):
        # print(dataset[i]['title'])
        mini_df = get_genres(dataset[i]['id'])
        # print(mini_df.head())

        # Append DataFrame for the current movie to the overall DataFrame of genres and id's
        # Also drop the duplicates
        df = pd.concat([df, mini_df]).drop_duplicates(subset=['genre_id'], keep='first')
    
    print(df.head(25))

    df.reset_index(names=['id'])

    print('\n', df.head(25))


def get_financials(movie_id: int):
    
    # url = f'https://api.themoviedb.org/3/movie/{movie_id}/rating'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=rating'
    
    # headers = dictionary of HTTP headers to send to the specified url
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {tmdb_api_read_access_token}'
    }

    response = requests.get(url, headers=headers)
    # print(response)

    # Check that request went through (i.e., if API request was successful)
    if response.status_code == 200:
        # Get JSON object of the request result
        array = response.json()
        # Convert from Python to JSON
        text = json.dumps(array)
        # Convert from JSON back to Python
        dataset_page = json.loads(text)

    else:
        return 'API Error'        

    # print('Creating the DataFrame...')
    # Create empty dataframe with headers
    df = pd.DataFrame(columns=['id', 'revenue', 'budget', 'runtime'])

    # print(dataset_page)
    
    # print('Grabbing the financial information...')
    df.loc[0] = [dataset_page['id'], dataset_page['revenue'],
                 dataset_page['budget'], dataset_page['runtime']]
       
    # print(df.head())

    return df


def get_popular_movies_financials(dataset: pd.DataFrame):

    for row in dataset:
        print(row)

    # # For each movie in the dataset, add its info to the dataframe
    # # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#setting-with-enlargement
    # print('Adding genre information to the DataFrame...')
    # for i in range(len(dataset)):
    #     # print(dataset[i]['title'])
    #     mini_df = get_genres(dataset[i]['id'])
    #     # print(mini_df.head())

    #     # Append DataFrame for the current movie to the overall DataFrame of genres and id's
    #     # Also drop the duplicates
    #     df = pd.concat([df, mini_df]).drop_duplicates(subset=['genre_id'], keep='first')
    
    # print(df.head(25))

    # df.reset_index(names=['id'])

    # print('\n', df.head(25))


def write_movie_file_to_postgres(file_name, dataset):
    '''
    Function to read a JSON object returned from an API request from TMDB to get 
    information about the most popular movies on the website
    '''

    # csv_file = open(file_name, 'a')
    # csv_writer = csv.writer(csv_file)
    
    print('Starting movie information extraction...')
    # print('Creating the Postgres engine...')
    # # Need to convert this DDL statement into something Postgres will understand
    # #   - Via create_engine([database_type]://[user]:[password]@[hostname]:[port]/[database], con=[engine])
    # engine = create_engine(f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_database}')
    # # print(engine)
    # # print(engine.connect())

    print('Creating the DataFrame...')
    # Create empty dataframe with headers
    df = pd.DataFrame(columns=['id', 'title', 'original_language', 'popularity', 
                               'release_date', 'genre_ids', 'vote_average', 'vote_count'])
    print(df.head())

    # For each movie in the dataset, add its info to the dataframe
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#setting-with-enlargement
    print('Adding movie information to the DataFrame...')
    for i in range(len(dataset)):
        # print(dataset[i]['title'])
        df.loc[i] = [dataset[i]['id'], dataset[i]['title'], dataset[i]['original_language'], 
                     dataset[i]['popularity'], dataset[i]['release_date'], dataset[i]['genre_ids'],
                     dataset[i]['vote_average'], dataset[i]['vote_count']]
        
    # Convert release_date to datetime
    df.release_date = pd.to_datetime(df.release_date)
    
    # Get financial data per movie id
    print('Creating the financial DataFrame...')
    # Create empty dataframe with headers
    financial_df = pd.DataFrame(columns=['id', 'revenue', 'budget', 'runtime'])

    for i in range(len(df['id'])):
        # print(df.iloc[i]['id'])
        financial_df_row = get_financials(df.iloc[i]['id'])
        # print(financial_df_row)
        # Append DataFrame for the current movie to the overall DataFrame of genres and id's
        # Also drop the duplicates
        financial_df = pd.concat([financial_df, financial_df_row]).drop_duplicates(subset=['id'], keep='first')        

    # print(financial_df.head())

    # https://stackoverflow.com/questions/26645515/pandas-join-issue-columns-overlap-but-no-suffix-specified
    df = df.merge(financial_df, on='id', how='left')
    print(df.head())

    # # print(df[:5])
    # # print(df.dtypes)
    # # print(df.describe())
    # # print(df.isnull().sum())

    # # # Create the path of where to store the parquet file
    # # # - Use .as_posix() for easier GCS and BigQuery access
    # # # https://stackoverflow.com/questions/68369551/how-can-i-output-paths-with-forward-slashes-with-pathlib-on-windows
    # # path = Path(f'data/{file_name}.parquet').as_posix()
    # # # path_csv = Path(f'data/{file_name}.csv')  # .as_posix()
    # # # print(f'PATH: {path.as_posix()}')

    # # # Create the data directory if it does not exist
    # # # https://stackoverflow.com/questions/23793987/write-a-file-to-a-directory-that-doesnt-exist
    # # os.makedirs(os.path.dirname(path), exist_ok=True)

    # # # Convert the DataFrame to a zipped parquet file and save to specified location
    # # print('Converting DataFrame to a parquet file...')
    # # df.to_parquet(path, compression='gzip')
    # # # df.to_csv(path_csv)

    # # Get the header/column names
    # header = df.head(n=0)
    # # print(header)

    # # Drop dependent tables
    # # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
    # # Use engine.begin(), NOT engine.connect(), which is deprecated
    # # https://stackoverflow.com/questions/75252652/python-sqlalchemy-postgresql-deprecated-api-features
    # with engine.begin() as conn:
    #     conn.execute(text(f'DROP TABLE if exists {postgres_movies_table_name} cascade'))

    # # Add the column headers to the green_taxi_data table in the database connection, and replace the table if it exists
    # print('Adding move information table column headers...')
    # header.to_sql(name=postgres_movies_table_name, con=engine, if_exists='replace')

    # # Add the movie info data
    # print('Loading in movie information data...')
    # df.to_sql(name=postgres_movies_table_name, con=engine, if_exists='append')


if __name__ == '__main__':
    # get_popular_movies()
    popular_movies_list = get_popular_movies()
    # get_popular_movies_genres(popular_movies_list)

    # The Meg 2
    # get_movie_info(615656)
    # get_movie_info2(615656)
    get_genres(615656)
    get_financials(615656)
    write_movie_file_to_postgres('test', popular_movies_list)
    # get_popular_movies_financials(popular_movies_list)