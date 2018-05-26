import gpxpy
import matplotlib.pyplot as plt
archivo = 'mission_complete.gpx'
gpx_file = open('C:\\Users\\David\\eclipse-workspace\\PX4Plotter\\mission_complete.gpx', 'r') 
gpx = gpxpy.parse(gpx_file) 
lat = []
long = []
for track in gpx.tracks: 
    for segment in track.segments: 
        for point in segment.points: 
            lat.append(point.latitude)
            long.append(point.longitude)
fig, ax = plt.subplots()
ax.set_title('GPS Track')
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.plot(long,lat,'--', linewidth=2)
ax.grid(True)
plt.show()   