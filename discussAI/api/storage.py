""" Storage Settings to handle File uploads """
import os
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    """ Storage settings for Azure """
    account_name = 'discussai'
    account_key = os.environ['AZURE_KEY']
    azure_container = 'media'
    expiration_secs = None
