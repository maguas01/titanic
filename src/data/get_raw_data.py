# -*-  coding: utf-8 -*-
#imports
import requests
from requests import session
import os
from dotenv import load_dotenv, find_dotenv
import logging

#payload for post request
payload = {
    'action' : 'login', 
    'username' : os.environ.get("kaggle_username"),
    'password' : os.environ.get("kaggle_password")
}

def extract_data(url, file_path) : 
    '''
    extract data from kaggle
    '''
    #set up a session 
    with session() as c : 
        c.post('https://www.kaggle.com/account/login',data=payload)
        #open a file to write to 
        with open(file_path, 'w') as handle : 
            response = c.get(url, stream=True)
            for block in response.iter_content(1024) : 
                handle.write(block)
                
def main(project_dir) : 
    '''
    main method
    '''
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')
    
    #urls
    train_url = 'https://www.kaggle.com/c/titanic/train.csv'
    test_url = 'https://www.kaggle.com/c/titanic/test.csv'
    
    # file paths
    raw_data_path = os.path.join(os.path.pardir, 'data', 'raw')
    train_data_path = os.path.join(raw_data_path, 'train.csv')
    test_data_path = os.path.join(raw_data_path, 'test.csv')
    
    #extract data
    extract_data(train_url, train_data_path)
    extract_data(test_url, test_data_path)
    logger.info('downloaded the raw training and test data')
    
if __name__ == '__main__': 
    project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
    
    #logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    #find the .env
    dotenv_path = find_dotenv()
    #load the variables 
    load_dotenv(dotenv_path)
    
    
    #call main
    main(project_dir)