import json
import pandas as pd
import requests
import psycopg2
import sys


def get_connection():
    """ Connect to the database server
    Args:
        conn_string: database connection string
    Returns:
        connection object
    """
    conn = None
    try:
        # logger.info('Connecting to the database ...')
        conn = psycopg2.connect(
            user="user",
            password="dbpassword",
            host="127.0.0.1",
            port="5000",
            database="dbname")
    except Exception as e:
        logger.error(e)
    return conn


def insert_data():
    query_users = """INSERT into users(phone, name, department) VALUES(%s, %s, %s) returning id"""
    query_location = """INSERT into location(type, parent, name, latitude, longitude) VALUES(%s, %s, %s, %s, %s) returning id"""
    user_location_query = """INSERT into user_location(user_id, location_id) VALUES(%s, %s)"""

    connection = get_connection()
    cursor = connection.cursor()
        
    # for AH&VS
    df = pd.read_csv(r'/root/data/n8n-demo-apis/AH&VS.csv',encoding='utf-8',skiprows = 1, header=None)
    df = df.values.tolist()
    for d in df:
        print("######################################################################")
        cursor.execute(query_users, (d[5], d[4],"AH&VS"))
        user_id = cursor.fetchone()[0]
        if not pd.isnull(d[2]):
            cursor.execute(query_location, ("Block", d[1], d[2], None, None))
            location_id = cursor.fetchone()[0]
            cursor.execute(user_location_query, (user_id, location_id))
        if not pd.isnull(d[3]):
            cursor.execute(query_location, ("Block", d[1], d[3], None, None))
            location_id = cursor.fetchone()[0]
            cursor.execute(user_location_query, (user_id, location_id))
        connection.commit()
        print("######################################################################")

    # for Fishery
    df = pd.read_csv(r'/root/data/n8n-demo-apis/fisheries.csv',encoding='utf-8',skiprows = 1, header=None)
    df = df.values.tolist()
    for d in df:
        print("######################################################################")
        cursor.execute(query_users, (d[7], d[6],"Fisheries"))
        user_id = cursor.fetchone()[0]
        if not pd.isnull(d[2]):
            cursor.execute(query_location, ("Block", d[1], d[2], None, None))
            location_id = cursor.fetchone()[0]
            cursor.execute(user_location_query, (user_id, location_id))
        if not pd.isnull(d[3]):
            cursor.execute(query_location, ("Block", d[1], d[3], None, None))
            location_id = cursor.fetchone()[0]
            cursor.execute(user_location_query, (user_id, location_id))
        if not pd.isnull(d[4]):
            cursor.execute(query_location, ("Block", d[1], d[3], None, None))
            location_id = cursor.fetchone()[0]
            cursor.execute(user_location_query, (user_id, location_id))
        if not pd.isnull(d[5]):
            cursor.execute(query_location, ("Block", d[1], d[3], None, None))
            location_id = cursor.fetchone()[0]
            cursor.execute(user_location_query, (user_id, location_id))
        connection.commit()
        print("######################################################################")
        
    # for FARD
    df = pd.read_csv(r'/root/data/n8n-demo-apis/fard.csv',encoding='utf-8',skiprows = 1, header=None)
    df = df.values.tolist()
    for d in df:
        print("######################################################################")
        cursor.execute(query_users, (d[4], d[3],"FARD"))
        user_id = cursor.fetchone()[0]
        if not pd.isnull(d[2]):
            cursor.execute(query_location, ("Block", d[1], d[2], None, None))
            location_id = cursor.fetchone()[0]
            cursor.execute(user_location_query, (user_id, location_id))
        connection.commit()
        print("######################################################################")


"""CREATE SCHEMA REQUESTS
    POST: http://127.0.0.1:5001/v2/query
    Content-Type application/json
    X-Hasura-Role admin
    x-hasura-admin-secret <admin-secret>
** For Location table
{
    "type": "run_sql",
    "args": {
        "source": "default",
        "sql": "CREATE TABLE IF NOT EXISTS location (id serial NOT NULL PRIMARY KEY, type varchar(50) NULL, parent varchar(50) NULL, name varchar(50) NULL, latitude varchar(50) NULL, longitude varchar(50) NULL);"
    }
}
** For Users table
{
    "type": "run_sql",
    "args": {
        "source": "default",
        "sql": "CREATE TABLE IF NOT EXISTS users (id serial NOT NULL PRIMARY KEY, phone varchar(50) NULL, name varchar(255) NULL, department varchar(50) NULL);"
    }
}
** For Relation Table
{
    "type": "run_sql",
    "args": {
        "source": "default",
        "sql": "CREATE TABLE user_location(id serial NOT NULL PRIMARY KEY,user_id INT,location_id INT,CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id),CONSTRAINT fk_location FOREIGN KEY(location_id) REFERENCES location(id));"
    }
}
"""


if __name__ == '__main__':
    globals()[sys.argv[1]]()
