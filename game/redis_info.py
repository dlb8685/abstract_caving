from django.conf import settings

REDIS_HOST = settings.CACHES['default']['LOCATION'].split(':')[0]
REDIS_PORT = settings.CACHES['default']['LOCATION'].split(':')[1]
REDIS_DB = settings.CACHES['default']['OPTIONS']['DB']
REDIS_PASSWORD = settings.CACHES['default']['OPTIONS']['PASSWORD']