import os
import re

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
RELATIVE_PATH_TO_RAW_DATA_FOLDER = '../raw/'
PATH_TO_RAW_DATA_FOLDER = os.path.join(CURRENT_PATH,
									   RELATIVE_PATH_TO_RAW_DATA_FOLDER)

class Importor(object):

	def __init__(self):
		print "hello world"
		self.payload = DataPayLoad()

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
					self.payload.set_target_radii(line[line.index(': ') + 2 : line.index('km') + 2])
				elif line.startswith('Center geodetic'):
					self.payload.set_center_geoetic(line[line.index(': ') + 2 : line.index(' {')])
				elif line.startswith('Center radii'):
					self.payload.set_center_radii(line[line.index(': ') + 2 : line.index('km') + 2])
				elif line.startswith('Target primary'):
					self.payload.set_target_primary(line[line.index(': ') + 2 : ].strip())
				elif line.startswith('$$SOE'):
					filtering_attr = False
			else:
				if line.startswith('$$EOE'):
					break;
				self._filter_RA_DEC(line)

	def _filter_RA_DEC(self, line):
		tokens = line.split(',')
		date_string = tokens[1]
		ra = float(tokens[4])
		dec = float(tokens[5])
		lt = float(tokens[6])
		print lt


	def get_RA_DEC(self, file_stream):
		file_stream = "$$SOE here is my text $$EOE"
		print re.findall(r'$$SOE(.*?)$$EOE',file_stream)


class DataPayLoad(object):

	def __init__(self):
		print "hello! I am payload"
		self.attr = dict()
		self.data = dict()

	def set_target_body_name(self, name):
		self.attr['target_body_name'] = name

	def set_target_body_code(self, code):
		self.attr['target_body_code'] = code

	def set_center_body_name(self, name):
		self.attr['target_center_body_name'] = name

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


if __name__ == "__main__":
    importer = Importor()
    file_list = importer._get_file_list()
    importer._get_subject_information(file_list)
    print importer.payload.get_attr()
