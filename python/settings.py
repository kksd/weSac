import os
from asteroid import asteroid

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

if os.environ.get('PORT'):
    SERVER_NAME = 'www.thepans.info'
else:
    SERVER_NAME = 'localhost:5000'
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'user'
    MONGO_PASSWORD = 'user'
    MONGO_DBNAME = 'eve'

DOMAIN = {
    'asteroid' : asteroid,
}
