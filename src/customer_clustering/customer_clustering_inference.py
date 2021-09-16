import os
import pickle
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.base import BaseEstimator
from sklearn.preprocessing import Normalizer

def __load_csv(file_name: str, index_col: str = None) -> pd.DataFrame:
        to_return = pd.read_csv(f"{os.getenv('PROJ_REPOS')}/data/{file_name}", encoding='latin1', index_col=index_col)
        return to_return

class DataTransformer:

    def __init__(self) -> None:
        pass
    
    def __to_unique_sorted_list(array: np.ndarray) -> list:
        to_return = list(set(array))
        to_return.sort()
        for i, item in enumerate(to_return):
            to_return[i] = item.replace(' ','_')
        return to_return

    def __create_customer_purchase_df_outline(self, customers, countries, stock_codes) -> pd.DataFrame:
        customer_df_outline = {}
        customer_df_outline['CustomerID'] = customers
        for country in countries:
            customer_df_outline[country] = 0
        for stock_code in stock_codes:
            customer_df_outline[stock_code] = 0
        to_return = pd.DataFrame(customer_df_outline)
        return to_return
    
    def transform_data(self, customer_ids: list):
        pass

class Predictor:

    def load_pca_model(self, pca_model_file_name: str) -> PCA:
        model = None
        with open(f"{os.getenv('PROJ_REPOS')}models/{pca_model_file_name}", "rb") as file:
            model = pickle.load(file)
        return model

    def load_clustering_model(self, clustering_model_file_name: str) -> BaseEstimator:
        model = None
        with open(f"{os.getenv('PROJ_REPOS')}models/{clustering_model_file_name}", "rb") as file:
            model = pickle.load(file)
        return model

    def __init__(self, pca_model_file_name: str, clustering_model_file_name: str) -> None:
        self.pca_model = self.load_pca_model(pca_model_file_name)
        self.clustering_model = self.load_clustering_model(clustering_model_file_name)

    def predict(self) -> dict:
        pass
