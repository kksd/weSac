import webapp2
import json
from google.appengine.ext import db
from models import *

class TestView(webapp2.RequestHandler):

    def get(self):
        latitude = self.request.get('lat')
        longitude = self.request.get('lon')
        id = self.request.get('id')

        q = db.Query(Asteroid)
        q.filter('target_body_code =', id)
        x = list()
        print '======here====='
        for asteroid in q.run():
            print '======'
            x.append(asteroid.target_body_code)
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


def asteroid_converter(asteroid):
    result = dict()
    result['target_body_name'] = asteroid.target_body_name
    result['target_body_code'] = asteroid.target_body_code
    result['center_body_name'] = asteroid.center_body_name
    result['target_radii'] = asteroid.target_radii
    result['center_geoetic'] = asteroid.center_geoetic
    result['center_radii'] = asteroid.center_radii
    result['target_primary'] = asteroid.target_primary
    return result


class InfoView(webapp2.RequestHandler):

    def get(self):
        id = self.request.get('id')

        if (id is None or len(id) <= 0):
            self.error(400)
            # self.response.out.write("No latitude or longitude given")
            return

        q = db.Query(Asteroid)
        q.filter('target_body_code =', id)
        result = dict()
        for asteroid in q.run():
            result = asteroid_converter(asteroid)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))


class ListQuery(webapp2.RequestHandler):

    def get(self):
        id = self.request.get('id')

        if (id is None or len(id) <= 0):
            self.error(400)
            # self.response.out.write("No latitude or longitude given")
            return

        q = db.Query(Asteroid)
        result = list()
        for asteroid in q.run():
            result.append(asteroid.target_body_code)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))