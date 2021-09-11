# Online-Retail

Currently a WIP project where I am exploring the data in an online retail data set.  

Website found: https://archive.ics.uci.edu/ml/datasets/Online+Retail  
Source: Dr Daqing Chen, Director: Public Analytics group. chend '@' lsbu.ac.uk, School of Engineering, London South Bank University, London SE1 0AA, UK.  
Abstract: This is a transnational data set which contains all the transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail.  

### Latest progress  

After creating a new data set where each row represents a customer, normalizing the data (by row), performing principle component analysis to get two principle components, and performing BIRCH clustering on the two principle components, four distinct groups of customers have been found.  

Script to generate transformed data sets is in src/data_processing/data_generator.py  
Notebook that led to the development of this script (has visualizations of clustering) can be found in notebooks/dataset_transformation.ipynb  
