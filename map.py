from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from random import randint
from random import randrange

m = Basemap(projection='kav7', resolution='c', lon_0=0)

#m.drawcoastlines()
m.drawmapboundary(fill_color='#CEEEFD')
m.fillcontinents(color='#A0C798',lake_color='#CEEEFD')


points = [ [-0.1271, 51.5063],[-99.1277, 19.4285],[-82.4646, 27.9709],[-115.136, 36.175],[-3.7058, 40.4203],[-70.6479, -33.463],[-0.1271, 51.5063],[-74.1178, 4.6564],[2.3412, 48.8569],[113.9174, 0.1097],[120.7391, 15.5931],[44.5651, 24.2599],[44.5651, 24.2599],[-0.28003184, 51.55693585],[27.80949255, 41.15201728] ]
for i in points:
	lat = i[1]
	lon = i[0]
	x, y = m(lon, lat)
	m.plot(x, y, 'bo', markersize=randint(1,15))
	"""lon = randrange(-180, 180)
	lat = randrange(-90, 90)
	x,y = m(lon, lat)
	m.plot(x, y, 'bo', markersize=randint(1, 30))"""

	
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()