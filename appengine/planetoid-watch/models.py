from google.appengine.ext import db

class Pet(db.Model):
    name = db.StringProperty(required=True)
    type = db.StringProperty(required=True, choices=set(["cat", "dog", "bird"]))
    birthdate = db.DateProperty()
    weight_in_pounds = db.IntegerProperty()
    spayed_or_neutered = db.BooleanProperty()

class Asteroid(db.Model):
    target_id = db.StringProperty(required=True)
    target_body_name = db.StringProperty(required=True)
    target_radii = db.StringProperty(required=True)
    center_geoetic = db.StringProperty(required=True)
    center_radii = db.StringProperty(required=True)
    target_primary = db.StringProperty(required=True)

class AsteroidLocation(db.Model):
    timestamp = db.DateTimeProperty(required=True)
    ra = db.FloatProperty(required=True)
    dec = db.FloatProperty(required=True)
    lt = db.FloatProperty(required=True)
