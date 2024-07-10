import sys

from prem_pred.exception import InsPremException
from prem_pred.logger import logging

import os
from prem_pred.constants import DATABASE_NAME, MONGODB_URL_KEY
import pymongo
import certifi

import base64

ca = certifi.where()

class MongoDBClient:
    """
    Class Name :   export_data_into_feature_store
    Description :   This method exports the dataframe from mongodb feature store as dataframe 
    
    Output      :   connection to mongodb database
    On Failure  :   raises an exception
    """
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY) #Read the CS
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                mongo_db_full_url = f"mongodb+srv://{MONGODB_URL_KEY}@cluster0.47dro4s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
                conv_to_bytes = bytes(mongo_db_full_url, 'utf-8')
                encode = base64.b64encode(conv_to_bytes)
                decode = base64.b64decode(encode).decode()
                # MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                MongoDBClient.client = pymongo.MongoClient(decode, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            #logging.info(f"MongoDB URL: {mongo_db_url}") # my comments for debug
            #logging.info(f"client: {self.client}") # my comments for debug
            #logging.info(f"database: {self.database}") # my comments for debug
            #logging.info(f"database name: {self.database_name}") # my comments for debug
            logging.info("MongoDB connection succesfull")
        except Exception as e:
            raise InsPremException(e,sys)