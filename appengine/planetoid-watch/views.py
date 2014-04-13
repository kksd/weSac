import webapp2
import json
from google.appengine.ext import db
from models import *

class TestView(webapp2.RequestHandler):

    def get(self):
        latitude = self.request.get('lat')
        longitude = self.request.get('lon')
        target_id = self.request.get('id')

        result = None
        q = db.Query(Asteroid)
        q.filter('target_id =', target_id)
        for asteroid in q.run():
            result = {
                info : asteroid
            }

            #if (latitude is None or len(latitude) <= 0 or
        #    longitude is None or len(longitude) <= 0):
        #    self.error(400)
            # self.response.out.write("No latitude or longitude given")
        #    return

        # do some calcs
        #result = {
        #    "latitude" : latitude,
        #    "longitude" : longitude,
        #    "data" : [1, 2, 3, "abc"],
        #    "song": x
        #}
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))
