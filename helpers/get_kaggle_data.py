import os
import logging

def kaggle_download(dataset):
    """
    Function to download kaggle datasets

        :dataset: str kaggle address

    """
    logging.info('Download of %s will start', dataset)

    os.system(f"kaggle datasets download -d {dataset}")

    # Make directory to unzip data
    os.system("mkdir 'data'")

    # Unzip data and store it in data folder
    dataset = dataset[dataset.find('/')+1:]
    os.system(f'unzip {dataset}.zip -d data')

    logging.info('Download completed')
