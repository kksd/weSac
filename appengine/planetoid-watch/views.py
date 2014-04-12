import webapp2
import json

class TestView(webapp2.RequestHandler):

    def get(self):
        latitude = self.request.get('lat')
        longitude = self.request.get('lon')

        if (latitude is None or len(latitude) <= 0 or 
            longitude is None or len(longitude) <= 0):
            self.error(400)
            # self.response.out.write("No latitude or longitude given")
            return

        # do some calcs
        result = {
            "latitude" : latitude,
            "longitude" : longitude,
            "data" : [1, 2, 3, "abc"]
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(result))
