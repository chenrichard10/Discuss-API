from django.conf import settings
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'discussai'
    account_key = 'WF7rUTt3C9q8w3EqNVufYHX5YsPtrt91WuQ6NuZZWi6GTAKi+Q9e8YknUblaqbL4UMYYVbequBsl/eHAWLK9aw=='
    azure_container = 'media'
    expiration_secs = None
