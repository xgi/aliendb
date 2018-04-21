import logging

# raise logger level for tests to reduce noise
logger = logging.getLogger('django.request')
logger.setLevel(logging.ERROR)