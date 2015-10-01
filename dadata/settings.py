from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

DADATA_API_URL = getattr(settings, 'DADATA_API_URL', 'https://dadata.ru/api/v2')
DADATA_API_TOKEN = getattr(settings, 'DADATA_API_TOKEN', None)
    
if not DADATA_API_TOKEN:
    raise ImproperlyConfigured("""API token are required. 
                                Please, check project settings for the DADATA_API_TOKEN. 
                                """)
