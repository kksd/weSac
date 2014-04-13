from pymongo import MongoClient
from datetime import datetime
from collections import defaultdict
from flask import Response
from flask import request
import flask
import math
import json

client = MongoClient()
db = client.eve


class Hacker(object):

	def hack(self, app):
		#This get current distance for all asteroids
		@app.route('/current')
		def index():
			result = []
			#utc = datetime.utcnow()
			#year = utc.year
			#month = utc.month
			#day = utc.day
			#hour = utc.hour
			#minute = utc.minute
			#minute = int(math.floor(minute / 10.0) * 10.0)
			#minute = 10 * math.floor(utc.minute / 10)
			#now = datetime(year, month, day, hour, minute)
			utc = request.args.get('utc', '')
			utc = datetime.strptime(utc, '%Y-%b-%d %H:%M')
			for item in db.location.find({"time" : utc}):
				data = {
					'aid' : item['aid'],
					'lt' : item['lt']
				}
				result.append(data)
			
			return Response(json.dumps(result), mimetype='application/json')

