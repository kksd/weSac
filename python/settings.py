import os
from asteroid import asteroid
from location import location

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

if os.environ.get('PORT'):
    SERVER_NAME = 'www.thepans.info'
else:
    SERVER_NAME = '10.172.248.91:8080'
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'user'
    MONGO_PASSWORD = 'user'
    MONGO_DBNAME = 'eve'

DOMAIN = {
    'asteroid' : asteroid,
    'location' : location
}