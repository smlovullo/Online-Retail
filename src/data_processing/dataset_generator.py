import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import PCA
from sklearn.cluster import Birch
from dotenv import load_dotenv
load_dotenv()

def save_csv(data_frame: pd.DataFrame, file_name: str) -> None:
    data_frame.to_csv(f"{os.getenv('PROJ_REPOS')}\\data\\{file_name}")

def load_csv(file_name: str, index_col: str = None) -> pd.DataFrame:
    to_return = pd.read_csv(f"{os.getenv('PROJ_REPOS')}\\data\\{file_name}", encoding='latin1', index_col=index_col)
    return to_return

def to_unique_sorted_list(array: np.ndarray) -> list:
    to_return = list(set(array))
    to_return.sort()
    for i, item in enumerate(to_return):
        to_return[i] = item.replace(' ','_')
    return to_return

def create_customer_purchase_df_outline() -> pd.DataFrame:
    customer_df_outline = {}
    customer_df_outline['CustomerID'] = customers
    for country in countries:
        customer_df_outline[country] = 0
    for stock_code in stock_codes:
        customer_df_outline[stock_code] = 0
    to_return = pd.DataFrame(customer_df_outline)
    return to_return

print('Reading in original data...')
online_retail_data = pd.read_excel("Online Retail.xlsx")
customer_data = online_retail_data.dropna(subset=['CustomerID'])
customer_data = customer_data.astype({'CustomerID': int})
customer_data = customer_data.astype({'CustomerID': str})

print('Gathering stock codes, customer IDs, and countries...')
stock_codes = to_unique_sorted_list(customer_data.StockCode.astype(str).values)
stock_codes = stock_codes[:-8]
customers = to_unique_sorted_list(customer_data.CustomerID.values)
countries = to_unique_sorted_list(customer_data.Country.values)

print('Creating outline of new customer-oriented data set...')
quantities_of_purchases_by_customer = create_customer_purchase_df_outline()

print('Populating new customer-oriented data set with values from the original data set...')
customer_countries = customer_data[['CustomerID', 'Country']].set_index(customer_data['CustomerID'])[['Country']].to_dict()['Country']
for customer_id, country in list(customer_countries.items()):
    quantities_of_purchases_by_customer.loc[quantities_of_purchases_by_customer['CustomerID'] == customer_id, country.replace(' ', '_')] = 1

customer_quantities_by_stockcode = customer_data[['CustomerID', 'StockCode', 'Quantity']].groupby(['CustomerID', 'StockCode']).sum().query('Quantity > 0').to_dict()
for customer_id, stock_code in list(customer_quantities_by_stockcode['Quantity'].keys()):
    if stock_code.replace(' ', '_') in stock_codes:
        quantities_of_purchases_by_customer.loc[quantities_of_purchases_by_customer['CustomerID'] == customer_id, stock_code.replace(' ', '_')] = customer_quantities_by_stockcode['Quantity'][(customer_id, stock_code)]

print('Saving first customer-oriented data set...')
quantities_of_purchases_by_customer = quantities_of_purchases_by_customer.set_index('CustomerID')
save_csv(quantities_of_purchases_by_customer, 'Customer_Purchases.csv')

quantities_of_purchases_by_customer_norm = load_csv('Customer_Purchases.csv', index_col='CustomerID')
quantities_of_purchases_by_customer = load_csv('Customer_Purchases.csv', index_col='CustomerID')

print('Creating normalized copy of customer-oriented data set...')
normalizer = Normalizer()
quantities_of_purchases_by_customer_norm[stock_codes] = normalizer.fit_transform(quantities_of_purchases_by_customer_norm[stock_codes])
print('Saving normalized copy of customer-oriented data set...')
save_csv(quantities_of_purchases_by_customer_norm, 'Customer_Purchases_Norm.csv')

print('Performing PCA on normalized customer data...')
pca_2d = PCA(n_components=2)
principle_components_2d = pca_2d.fit_transform(quantities_of_purchases_by_customer_norm)
principle_2d_df = pd.DataFrame(data=principle_components_2d, columns=['pc1', 'pc2'])
principle_2d_df = principle_2d_df.set_index(quantities_of_purchases_by_customer_norm.index)
print('Performing clustering on principle components of normalized customer data...')
clustering_model = Birch(threshold=0.01, n_clusters=4)
clustering_model.fit(principle_2d_df)
predictions = clustering_model.predict(principle_2d_df)
clusters = np.unique(predictions)
principle_2d_df['Cluster'] = predictions
print('Adding cluster labels to customer data sets...')
customers_clustered = principle_2d_df[['Cluster']].join(quantities_of_purchases_by_customer)
customers_clustered_norm = principle_2d_df[['Cluster']].join(quantities_of_purchases_by_customer_norm)

print('Saving clustering model...')
model_file_name = 'cluster_model.pkl'
with open(f"{os.getenv('PROJ_REPOS')}\\models\\{model_file_name}", 'wb') as file:
    pickle.dump(clustering_model, file)
print('Saving new versions of customer data sets with cluster labels...')
save_csv(customers_clustered, 'Customer_Purchases_Clusters.csv')
save_csv(customers_clustered_norm, 'Customer_Purchases_Clusters_Norm.csv')

print('Finished generating customer data sets')