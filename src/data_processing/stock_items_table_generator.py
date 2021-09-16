import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Read original xlsx file
file_path = f"{os.getenv('PROJ_REPOS')}/data/Online Retail.xlsx"
online_retail = pd.read_excel(file_path)
online_retail['StockCode'] = online_retail['StockCode'].astype(str)
online_retail['Description'] = online_retail['Description'].astype(str)

# Build a data frame of unique stock code and description pairs from data where Quantity > 0
stock_items_raw = online_retail.query('Quantity > 0')[['StockCode', 'Description']].drop_duplicates()

# If description is NaN, drop the pair
stock_items = stock_items_raw.dropna()

# Make stock codes all uppercase
stock_items.loc[:, 'StockCode'] = stock_items.loc[:, 'StockCode'].str.upper()

# If description is in lower case, drop the pair
stock_items.loc[:, 'StockCode'] = stock_items.loc[:, 'StockCode'].str.upper()
stock_items['Desc_isupper'] = list(map(lambda x: x.isupper(), stock_items['Description']))
stock_items = stock_items.query('Desc_isupper == True')[['StockCode', 'Description']]

# Get list of all unique stock codes
stock_codes = list(stock_items.StockCode.unique())
stock_codes.sort()

# Get list of stock codes that remove codes that do not represent a product
to_drop = [
    "AMAZONFEE",
    "C2",
    "DOT",
    "PADS",
    "POST",
    "S"
]
to_keep = list(stock_codes)
for entry in to_drop:
    to_keep.remove(entry)

# Create boolean column that represents whether or not a row's description contains more than one word
stock_items['multi_word'] = list(map(lambda desc: ' ' in desc, stock_items['Description']))
stock_items.query("multi_word == False")

# If an stock code does not represent a product, get rid of it
# If a row has a description of only one word, drop it
stock_items = stock_items[stock_items["StockCode"].isin(to_keep)].query("multi_word == True")[['StockCode', 'Description']]

# Otherwise, leave duplicates for one table; they share a stock code because they are highly similar products
stock_items = stock_items.sort_values('StockCode').reset_index()[['StockCode', 'Description']]
stock_items_all = stock_items

# Remove duplicate stock codes for another table; this table will have unique stock codes for each description
stock_items = stock_items.drop_duplicates('StockCode')

# Write data frames to csv files
stock_items_all.to_csv(f"{os.getenv('PROJ_REPOS')}/data/Stock_Items_All.csv")
stock_items.to_csv(f"{os.getenv('PROJ_REPOS')}/data/Stock_Items.csv")
