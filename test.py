import geopandas as gpd
from neighborhood import *

def ReturnGeoSpatialData(address, distance=1, distanceUnit='miles'):

    #location of the shape file
    infile_shp='./Shape_Files/Boston_Neighborhoods-shp'
    #geopandas read shape file and convert to geodataframe
    shp_gdf = gpd.read_file(infile_shp).to_crs(epsg=4326)

    #instantiate the class
    n = neighborhood_of_a_point(address, shp_gdf)

    #returns coordinates of the address
    n.coordinates_gdf.geometry

    #returns geometry of the shape
    n.loc_gdf.geometry

    n.set_buffer(distance, distanceUnit)
    #returns geometry of the radius around the address
    n.buffer_gdf.geometry

    #returns geometry of the shapes which intersect the radius around the address
    n.set_neighborhoods()
    n.neighborhoods_gdf.geometry

    return n

if __name__ == '__main__':
    # ReturnGeoSpatialData('150 Brookline Avenue, Boston, MA', 1, "miles")
    pass