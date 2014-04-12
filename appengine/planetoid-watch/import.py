import getpass
from datetime import datetime
from google.appengine.ext.remote_api import remote_api_stub
from models import *

def get_auth_creds_from_stdin():
    username = raw_input('Username:')
    password = getpass.getpass('Password:')
    return (username, password)

def config_remote_api(auth_func, appid):
    remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', 
        auth_func, str(appid) + '.appspot.com')

if __name__ == "__main__":
    import dev_appserver
    dev_appserver.fix_sys_path()
    config_remote_api(get_auth_creds_from_stdin, "planetoid-watch")

    # delete old data
    db.delete(Pet.all())
    db.delete(AsteroidLocation.all())
    db.delete(Asteroid.all())

    # sample pet data, simple use case
    Pet(name="Buddy", type="dog").put()
    Pet(name="Taz", type="cat").put()

    # import asteroid from dictionary
    asteroid_data = {
        "target_body_name" : "Test 123", 
        "center_body_name" : "Earth", 
        "target_radii" : "2.3 km", 
        "center_geoetic" : "Sample", 
        "center_radii" : "442 km", 
        "target_primary" : "Sun", 
    }
    asteroid = Asteroid(**asteroid_data)
    asteroid.put()

    # add a bunch of locations for the asteroid
    AsteroidLocation(asteroid=asteroid, timestamp=datetime(2014, 04, 11, 00, 00, 00), ra=1.23, dec=-4.53, lt=8.456).put()
    AsteroidLocation(asteroid=asteroid, timestamp=datetime(2014, 04, 11, 00, 00, 10), ra=1.43, dec=-4.63, lt=8.455).put()
    AsteroidLocation(asteroid=asteroid, timestamp=datetime(2014, 04, 11, 00, 00, 20), ra=1.53, dec=-4.73, lt=8.454).put()
    AsteroidLocation(asteroid=asteroid, timestamp=datetime(2014, 04, 11, 00, 00, 30), ra=1.83, dec=-4.83, lt=8.453).put()
