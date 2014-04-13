from pymongo import MongoClient
from datetime import datetime
from collections import defaultdict
from flask import Response
from flask import request
from calculator import Calculator
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
			utc = datetime.strptime(utc, '%Y-%m-%d %H:%M')

			lat = float(request.args.get('lat', ''))
			lon = float(request.args.get('lon', ''))

			for item in db.location.find({"time" : utc}):
				calculator = Calculator()
				answer = calculator.convert(item['ra'], item['dec'], lat, lon, item['lt'], utc)

				data = {
					'aid' : item['aid'],
					'lt' : item['lt'],
					'alt' : answer['altitude'],
					'azi' : answer['azimuth']
				}

				result.append(data)
			
			return Response(json.dumps(result), mimetype='application/json')

