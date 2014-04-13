from importer import Importer

from eve import Eve
app = Eve()

if __name__ == '__main__':
	importer = Importer()
	importer.do()
	app.run(host='0.0.0.0')
