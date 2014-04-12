import os
import re

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
RELATIVE_PATH_TO_RAW_DATA_FOLDER = '../raw/'
PATH_TO_RAW_DATA_FOLDER = os.path.join(CURRENT_PATH,
									   RELATIVE_PATH_TO_RAW_DATA_FOLDER)

class Importor(object):

	def __init__(self):
		print "hello world"
		self.data = DataPayLoad()

	def _get_file_list(self):
		
		ret = os.listdir(os.path.join(PATH_TO_RAW_DATA_FOLDER))
		return ret

	def _get_subject_information(self, file_list):
		for raw_file in file_list:
			path_to_the_file = os.path.join(PATH_TO_RAW_DATA_FOLDER,
											raw_file)
			with open(path_to_the_file, 'r') as f:
				lines = f.readlines()
				self.filter(lines)
				file_stream = f.read()
				print self.get_RA_DEC(file_stream)


	def filter(self, lines):
		for line in lines:
			if line.startswith('Target body name:'):
				tokens = line.split(' ')
				self.data.set_target_body_code(tokens[3])
				self.data.set_target_body_name(tokens[4])
			elif line.startswith('Center body name:'):
				tokens = line.split(' ')
				self.data.set_center_body_name(tokens[3])
			elif line.startswith('Target radii'):
				self.data.set_target_radii(line[line.index(': ') + 2 : line.index('km') + 2])
			elif line.startswith('Center geodetic'):
				self.data.set_center_geoetic(line[line.index(': ') + 2 : line.index(' {')])
			elif line.startswith('Center radii'):
				self.data.set_center_radii(line[line.index(': ') + 2 : line.index('km') + 2])
			elif line.startswith('Target primary'):
				self.data.set_target_primary(line[line.index(': ') + 2 : ].strip())

	def get_RA_DEC(self, file_stream):
		file_stream = "$$SOE here is my text $$EOE"
		print re.findall(r'$$SOE(.*?)$$EOE',file_stream)


class DataPayLoad(object):

	def __init__(self):
		print "hello! I am payload"
		self.data = {}

	def set_target_body_name(self, name):
		self.data['target_body_name'] = name

	def set_target_body_code(self, code):
		self.data['target_body_code'] = code

	def set_center_body_name(self, name):
		self.data['target_center_body_name'] = name

	def set_target_radii(self, rad):
		self.data['target_radii'] = rad

	def set_center_geoetic(self, geo):
		self.data['center_geoetic'] = geo

	def set_center_radii(self, rad):
		self.data['center_radii'] = rad

	def set_target_primary(self, primary):
		self.data['target_primary'] = primary

	def add_RA_DEC(self):
		pass

	def get_dict(self):
		return self.data

if __name__ == "__main__":
    importer = Importor()
    file_list = importer._get_file_list()
    importer._get_subject_information(file_list)
    print importer.data.get_dict()
