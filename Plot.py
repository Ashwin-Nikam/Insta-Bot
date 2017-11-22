import gmplot

latitudes = []
longitudes = []

def plot_points(locations):
    for location in locations:
        latitudes.append(location[0])
        longitudes.append(location[1])
        gmap = gmplot.GoogleMapPlotter(latitudes[0], longitudes[0], zoom=1)
        gmap.scatter(latitudes, longitudes, '#FF6666', edge_width=10)
        gmap.draw("map.html")