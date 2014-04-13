from pymongo import MongoClient
from datetime import datetime
import flask

client = MongoClient()
db = client.eve


class Hacker(object):

	def hack(self, app):
		@app.route('/current')
		def index():
			return 'Hello World'

