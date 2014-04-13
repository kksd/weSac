import os
from datetime import datetime
import re
import getpass
from google.appengine.ext.remote_api import remote_api_stub
from models import *
import dev_appserver

def get_auth_creds_from_stdin():
    username = raw_input('Username:')
    password = getpass.getpass('Password:')
    return (username, password)

def config_remote_api(auth_func, appid):
    remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', 
        auth_func, str(appid) + '.appspot.com')


CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
RELATIVE_PATH_TO_RAW_DATA_FOLDER = 'raw/'
PATH_TO_RAW_DATA_FOLDER = os.path.join(CURRENT_PATH,
                                       RELATIVE_PATH_TO_RAW_DATA_FOLDER)

class Importor(object):

    def __init__(self):
        print "hello world"
        self.payload = DataPayLoad()
        
        dev_appserver.fix_sys_path()
        config_remote_api(get_auth_creds_from_stdin, "planetoid-watch")

        # delete old data
        #db.delete(Pet.all())
        db.delete(AsteroidLocation.all())
        db.delete(Asteroid.all())

        # sample pet data, simple use case
        #Pet(name="Buddy", type="dog").put()
        #Pet(name="Taz", type="cat").put()


        

    def _get_file_list(self):
        
        ret = os.listdir(os.path.join(PATH_TO_RAW_DATA_FOLDER))
        return ret

    def readAsteroids(self, file_list):
        for raw_file in file_list:
            path_to_the_file = os.path.join(PATH_TO_RAW_DATA_FOLDER,
                                            raw_file)
            with open(path_to_the_file, 'r') as f:
                lines = f.readlines()
                self.read(lines)

    def read(self, lines):
        payload = DataPayLoad()
        filtering_attr = True
        for line in lines:
            if filtering_attr:
                if line.startswith('Target body name:'):
                    tokens = line.split(' ')
                    payload.set_target_id(tokens[3])
                    payload.set_target_body_name(tokens[4])
                elif line.startswith('Center body name:'):
                    tokens = line.split(' ')
                    #payload.set_center_body_name(tokens[3])
                elif line.startswith('Target radii'):
                    payload.set_target_radii(line[line.index(': ') + 2 : line.index('km') + 2])
                elif line.startswith('Center geodetic'):
                    payload.set_center_geoetic(line[line.index(': ') + 2 : line.index(' {')])
                elif line.startswith('Center radii'):
                    payload.set_center_radii(line[line.index(': ') + 2 : line.index('km') + 2])
                elif line.startswith('Target primary'):
                    payload.set_target_primary(line[line.index(': ') + 2 : ].strip())
                elif line.startswith('$$SOE'):
                    filtering_attr = False
            else:
                if line.startswith('$$EOE'):
                    break;
                payload.add_data(self.readAsteroidData(line))

        #store the payload
        asteroid = Asteroid(**payload)
        asteroid.put()
        data = payload.get_data
        for location in data:
            al = AsteroidLocation(asteroid=asteroid, **location)
            al.put()

    def readAsteroidData(self, line):
        tokens = line.split(',')
        date_time = self._get_datetime(tokens[0])
        ra = float(tokens[4])
        dec = float(tokens[5])
        lt = float(tokens[6])


        data = {'timestamp': date_time,
                'ra': ra,
                'dec': dec,
                'lt': lt}
        return data

    def _get_datetime(self, date_string):
        d = datetime.strptime(date_string.strip() , '%Y-%b-%d %H:%M:%S')
        return d

    def get_RA_DEC(self, file_stream):
        file_stream = "$$SOE here is my text $$EOE"
        print re.findall(r'$$SOE(.*?)$$EOE',file_stream)


class DataPayLoad(object):

    def __init__(self):
        print "hello! I am payload"
        self.attr = dict()
        self.data = list()

    def set_target_body_name(self, name):
        self.attr['target_body_name'] = name

    def set_target_id(self, id):
        self.attr['target_id'] = id

    #def set_center_body_name(self, name):
    #    self.attr['target_center_body_name'] = name

    def set_target_radii(self, rad):
        self.attr['target_radii'] = rad

    def set_center_geoetic(self, geo):
        self.attr['center_geoetic'] = geo

    def set_center_radii(self, rad):
        self.attr['center_radii'] = rad

    def set_target_primary(self, primary):
        self.attr['target_primary'] = primary

    def add_RA_DEC(self):
        pass

    def get_attr(self):
        return self.attr

    def add_data(self, data):
        self.data.append(data)

    def get_data(self):
        return self.data


if __name__ == "__main__":
    importer = Importor()
    file_list = importer._get_file_list()
    importer.readAsteroids(file_list)


    


    # print importer.payload.get_data()
