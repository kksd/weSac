import math

class Calculator():
	def hms2real(self, h, m, s):
		return 15.0 * (h + m/60.0 + s/3600.0)

	def dms2real(self, d, m, s):
		result = 0.0
		if d < 0.0:
			result = d - m/60.0 - s/3600.0
		else:
			result = d + m/60.0 + s/3600.0
		return result

	def meanSiderealTime(self, utc, lon):
		year = utc.year
		month = utc.month
		day = utc.day
		hour = utc.hour
		minute = utc.minute
		second = utc.second

		a = math.floor(year/100.0)
		b = 2.0 - a + math.floor(a/4.0)
		c = math.floor(365.25*year)
		d = math.floor(30.6001*(month + 1.0))


		jd = b + c + d - 730550.5 + day + (hour + minute/60.0 + second/3600.0)/24.0
		jt = jd/36525.0


		mst = 280.46061837 + 360.98564736629 * jd 
		mst = mst + 0.000387933 * jt * jt 
		mst = mst - jt * jt * jt / 38710000.0 
		mst = mst + lon

		if mst > 0.0:
			while mst > 360.0:
				mst = mst - 360.0
		else:
			while mst < 0.0:
				mst = mst + 360.0

		return mst 

	

	def convert(self, ra, dec, lat, lon, lt, dt):

		ha = self.meanSiderealTime(dt, lon) - ra

		if ha < 0:
			ha = ha + 360.0

		ha = ha * math.pi/180.0
		dec = dec * math.pi/180.0
		lat = lat * math.pi/180.0


		sin_alt = math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha)
		alt = math.asin(sin_alt)

		cos_az = (math.sin(dec) - math.sin(alt) * math.sin(lat)) / (math.cos(alt) * math.cos(lat))
		az = math.acos(cos_az)

		hrz_altitude = alt * 180.0 / math.pi
		hrz_azimuth = az * 180.0 / math.pi

		if math.sin(ha) > 0.0:
			hrz_azimuth = 360.0 - hrz_azimuth

		result = {
			'altitude' : hrz_altitude,
			'azimuth' : hrz_azimuth
		}
		return result









