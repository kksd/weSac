from datetime import datetime
from calculator import Calculator

calculator = Calculator()

ra = {'hour' : 1, 'minute' : 24, 'second' : 0 }
dec = {'degree' : 8, 'minute' : 49.796, 'second' : 0}
lat = {'degree' : 43, 'minute' : 27, 'second' : 0}
lon = {'degree' : -80, 'minute' : 29, 'second' : 0}
dt = datetime(2014, 4, 12, 20, 43, 0)

ra = calculator.hms2real(ra['hour'], ra['minute'], ra['second'])
dec = calculator.dms2real(dec['degree'], dec['minute'], dec['second'])
lat = calculator.dms2real(lat['degree'], lat['minute'], lat['second'])
lon = calculator.dms2real(lon['degree'], lon['minute'], lon['second'])

result = calculator.convert(ra, dec, lat, lon, 0, dt)
print result