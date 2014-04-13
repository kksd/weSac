import webapp2
import json
from google.appengine.ext import db
from models import *

class TestView(webapp2.RequestHandler):

    def get(self):
        latitude = self.request.get('lat')
        longitude = self.request.get('lon')

        q = db.Query(Asteroid)
        q.filter('target_body_name =', 'Test 123')
        x = None
        print '======here====='
        for asteroid in q.run():
            print '======'
            x = asteroid.target_body_name
        if (latitude is None or len(latitude) <= 0 or 
            longitude is None or len(longitude) <= 0):
            self.error(400)
            # self.response.out.write("No latitude or longitude given")
            return

        # do some calcs
        result = {
            "latitude" : latitude,
            "longitude" : longitude,
            "data" : [1, 2, 3, "abc"],
            "song": x
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))
