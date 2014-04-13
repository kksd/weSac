from importer import Importer
from hack import Hacker
from eve import Eve

app = Eve()

"""def before_returning_location(response):
	print response

def post_location_get(request, payload):
	lat = request.args.get('lat', '')
	lon = request.args.get('lon', '')
	time = payload.data

	print lat
	print lon
	print time

	#print request
	#print request.args.get('lat', '')
	#print payload.data
	#print payload['lt']
"""

if __name__ == '__main__':
	importer = Importer()
	hacker = Hacker()
	importer.do()

	hacker.hack(app)
	app.run(host='0.0.0.0')
