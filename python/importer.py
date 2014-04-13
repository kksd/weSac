import os
from pymongo import MongoClient
from datetime import datetime
from collections import defaultdict

DEBUG = False
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
RELATIVE_PATH_TO_RAW_DATA_FOLDER = 'raw/'
PATH_TO_RAW_DATA_FOLDER = os.path.join(CURRENT_PATH,
                                       RELATIVE_PATH_TO_RAW_DATA_FOLDER)
UNAVAILABLE = "(unavailable)"

class Importer(object):

    def _get_file_list(self):
        ret = os.listdir(os.path.join(PATH_TO_RAW_DATA_FOLDER))
        return ret

    def _get_datetime(self, date_string):
        d = datetime.strptime(date_string.strip() , '%Y-%b-%d %H:%M')
        return d


    def do(self):
        #Initialize Mongo DB
        client = MongoClient()
        db = client.eve
        db.drop_collection('asteroid')
        db.drop_collection('location')

        file_list = self._get_file_list()
        for raw_file in file_list:
            path_to_the_file = os.path.join(PATH_TO_RAW_DATA_FOLDER,
                                            raw_file)
            with open(path_to_the_file, 'r') as f:
                lines = f.readlines()
                
                #get asteroid
                a = defaultdict(int)

                filtering_attr = True
                for line in lines:
                    if filtering_attr:
                        if line.startswith('Target body name:'):
                            tokens = line.split(' ')
                            a['aid'] = tokens[3]
                            a['name'] = tokens[4]
                        elif line.startswith('Target radii'):
                            try:
                                value = line[line.index(': ') + 2 : line.index('km') + 2]
                            except:
                                value = UNAVAILABLE
                            a['radii'] = value
                        elif line.startswith('Target primary'):
                            try:
                                value = line[line.index(': ') + 2 : ].strip()
                            except:
                                value = UNAVAILABLE
                            a['primary'] = value
                        elif line.startswith('$$SOE'):
                            db.asteroid.insert(a)
                            filtering_attr = False
                    else:
                        if line.startswith('$$EOE'):
                            break;
                        l = defaultdict(int)
                        tokens = line.split(',')
                        l['time'] = self._get_datetime(tokens[0])
                        l['ra'] = float(tokens[4])
                        l['dec'] = float(tokens[5])
                        l['lt'] = float(tokens[6])
                        l['aid'] = a['id']
                        db.location.insert(l)
                




