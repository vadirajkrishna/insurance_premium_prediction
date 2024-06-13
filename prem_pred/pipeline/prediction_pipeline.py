import os
import sys

import numpy as np
import pandas as pd
from prem_pred.entity.config_entity import PremPredictorConfig
from prem_pred.entity.s3_estimator import PremPredEstimator
from prem_pred.exception import InsPremException
from prem_pred.logger import logging
from prem_pred.utils.main_utils import read_yaml_file
from pandas import DataFrame


class PremPredData:
    def __init__(self,
                age,
                sex,
                bmi,
                children,
                smoker,
                region
                ):
        """
        Usvisa Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.age = age
            self.sex = sex
            self.bmi = bmi
            self.children = children
            self.smoker = smoker
            self.region = region

        except Exception as e:
            raise InsPremException(e, sys) from e

    def get_prempred_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from PremPredData class input
        """
        try:
            
            prempred_input_dict = self.get_prempred_data_as_dict()
            return DataFrame(prempred_input_dict)
        
        except Exception as e:
            raise InsPremException(e, sys) from e


    def get_prempred_data_as_dict(self):
        """
        This function returns a dictionary from PremPredaData class input 
        """
        logging.info("Entered get_prempred_data_as_dict method as PremPredData class")

        try:
            input_data = {
                "age": [self.age],
                "sex": [self.sex],
                "bmi": [self.bmi],
                "children": [self.children],
                "smoker": [self.smoker],
                "region": [self.region],
            }

            logging.info("Created prempred data dict")

            logging.info("Exited get_prempred_data_as_dict method as PremPredData class")

            return input_data

        except Exception as e:
            raise InsPremException(e, sys) from e

class PremiumPredictor:
    def __init__(self,prediction_pipeline_config: PremPredictorConfig = PremPredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise InsPremException(e, sys)

    def predict(self, dataframe) -> float:
        """
        This is the method of PremiumPredictor
        Returns: Prediction in float format
        """
        try:
            logging.info("Entered predict method of PremiumPredictor class")
            # logging.info("dataframe is", dataframe) #for debug
            model = PremPredEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise InsPremException(e, sys)