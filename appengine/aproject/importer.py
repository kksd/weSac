import os
from datetime import datetime
import re
import getpass
from google.appengine.ext.remote_api import remote_api_stub
from models import *
import dev_appserver

def get_auth_creds_from_stdin():
    #username = raw_input('Username:')
    password = getpass.getpass('Password:')
    return ('aka.xchen@gmail.com', password)

def config_remote_api(auth_func, appid):
    remote_api_stub.ConfigureRemoteApi(None, '/_ah/remote_api', 
        auth_func, str(appid) + '.appspot.com')

DEBUG = False
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
RELATIVE_PATH_TO_RAW_DATA_FOLDER = 'raw/'
PATH_TO_RAW_DATA_FOLDER = os.path.join(CURRENT_PATH,
                                       RELATIVE_PATH_TO_RAW_DATA_FOLDER)
UNAVAILABLE = "(unavailable)"

class Importor(object):

    def __init__(self):
        print "hello world"
        self.payload = DataPayLoad()
        if not DEBUG:
            dev_appserver.fix_sys_path()
            config_remote_api(get_auth_creds_from_stdin, "eminent-yen-549")

            # delete old data
            db.delete(Pet.all())
            #db.delete(AsteroidLocation.all())
            #db.delete(Asteroid.all())

    def _get_file_list(self):
        
        ret = os.listdir(os.path.join(PATH_TO_RAW_DATA_FOLDER))
        return ret

    def _get_subject_information(self, file_list):
        for raw_file in file_list:
            print raw_file
            path_to_the_file = os.path.join(PATH_TO_RAW_DATA_FOLDER,
                                            raw_file)
            with open(path_to_the_file, 'r') as f:
                lines = f.readlines()
                self.filter(lines)
            print self.payload.get_attr()
            if not DEBUG:
                asteroid = Asteroid(**self.payload.attr)
                asteroid.put()
                for location in self.payload.data:
                    AsteroidLocation(asteroid=asteroid,
                                     code=location['code'],
                                     timestamp=location['timestamp'],
                                     ra=location['ra'],
                                     dec=location['dec'],
                                     lt=location['lt']).put()
            self.payload.clean_payload()
            break


    def filter(self, lines):
        filtering_attr = True
        for line in lines:
            if filtering_attr:
                if line.startswith('Target body name:'):
                    tokens = line.split(' ')
                    self.payload.set_target_body_code(tokens[3])
                    self.payload.set_target_body_name(tokens[4])
                elif line.startswith('Center body name:'):
                    tokens = line.split(' ')
                    self.payload.set_center_body_name(tokens[3])
                elif line.startswith('Target radii'):
                    try:
                        value = line[line.index(': ') + 2 : line.index('km') + 2]
                    except:
                        value = UNAVAILABLE
                    self.payload.set_target_radii(value)
                elif line.startswith('Center geodetic'):
                    try:
                        value = line[line.index(': ') + 2 : line.index(' {')]
                    except:
                        value = UNAVAILABLE
                    self.payload.set_center_geoetic(value)
                elif line.startswith('Center radii'):
                    try:
                        value = line[line.index(': ') + 2 : line.index('km') + 2]
                    except:
                        value = UNAVAILABLE
                    self.payload.set_center_radii(value)
                elif line.startswith('Target primary'):
                    try:
                        value = line[line.index(': ') + 2 : ].strip()
                    except:
                        value = UNAVAILABLE
                    self.payload.set_target_primary(value)
                elif line.startswith('$$SOE'):
                    filtering_attr = False
            else:
                if line.startswith('$$EOE'):
                    break;
                self._filter_RA_DEC_and_publish(line, self.payload.attr['target_body_code'])

    def _filter_RA_DEC_and_publish(self, line, target_body_code):
        tokens = line.split(',')
        date_time = self._get_datetime(tokens[0])
        ra = float(tokens[4])
        dec = float(tokens[5])
        lt = float(tokens[6])
        data = {'code': target_body_code,
                'timestamp': date_time,
                'ra': ra,
                'dec': dec,
                'lt': lt}
        self.payload.add_data(data)

    def _get_datetime(self, date_string):
        d = datetime.strptime(date_string.strip() , '%Y-%b-%d %H:%M')
        return d


class DataPayLoad(object):

    def __init__(self):
        print "hello! I am payload"
        self.attr = dict()
        self.data = list()

    def set_target_body_name(self, name):
        self.attr['target_body_name'] = name

    def set_target_body_code(self, code):
        self.attr['target_body_code'] = code

    def set_center_body_name(self, name):
        self.attr['center_body_name'] = name

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

    def clean_payload(self):
        # I need to do this because I was lazy
        self.attr = dict()
        self.data = list()


if __name__ == "__main__":
    importer = Importor()
    file_list = importer._get_file_list()
    importer._get_subject_information(file_list)
    # print len(importer.payload.get_attr())
    # print importer.payload.get_data()
