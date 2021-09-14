import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import wkt
import pandas as pd
import pathlib
pathlib.Path().resolve()

class neighborhood_of_a_point:

    def __init__(self, address, gdf=None):

        #geocode address string
        useCachedFile = True
        if address=="150 Brookline Avenue, Boston, MA":
            cachedFileName = "./Cached_CSV_Files/150_Brookline_Ave.csv"
        elif address=="200 Brookline Avenue, Boston, MA":
            cachedFileName = "./Cached_CSV_Files/200_Brookline_Ave.csv"
        elif address=="250 Brookline Avenue, Boston, MA":
            cachedFileName = "./Cached_CSV_Files/250_Brookline_Ave.csv"
        elif address=="300 Brookline Avenue, Boston, MA":
            cachedFileName = "./Cached_CSV_Files/300_Brookline_Ave.csv"
        elif address=="350 Brookline Avenue, Boston, MA":
            cachedFileName = "./Cached_CSV_Files/350_Brookline_Ave.csv"
        else:
            useCachedFile = False

        if useCachedFile==True:
            df = pd.read_csv(cachedFileName)
            df['geometry'] = df['geometry'].apply(wkt.loads)
            self.coordinates_gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
        else:
            self.coordinates_gdf = gpd.tools.geocode(address, provider="nominatim", user_agent='my_request')
        self.address = self.coordinates_gdf.address[0]
        self.coordinates = self.coordinates_gdf.geometry[0]

        #declare buffer and buffer radius (used for ring studies)
        self.buffer_radius = None
        self.buffer = None
        self.buffer_gdf = None
        #set initial buffer size to 0
        self.set_buffer(0)

        #declare core geodataframe and initialize if passed to constructor
        self.gdf = gdf

        #declare geodataframe which will contain the shape enclosing the coordinates of the address
        self.loc_gdf = None

        #if a geodataframe is passed to the constructor immediatly determine if it contains a shape containing the coordinates of the address
        if self.gdf is not None:
            self.set_loc_gdf()

        #declare neighborhoods geodataframe that will contain shapes from the core gdf which overlap the buffer (ring)
        self.neighborhoods_gdf = None

    def get_buffer(self):
        return self.buffer

    def set_buffer(self, d, metric='kilometers'):
        self.buffer_radius = d

        if metric == "miles":
            d *= (1.60934 * 1000)
        elif metric == 'kilometers':
            d *= 1000
        else:
            raise Exception("metric error")

        self.buffer = self.coordinates_gdf.to_crs(crs="EPSG:3174").buffer(d).to_crs(crs="EPSG:4269").geometry[0]
        df = {'buffer centroid': [self.address + " buffer"]}
        self.buffer_gdf = gpd.GeoDataFrame(df, geometry=[self.buffer])

    def plot_buffer(self):
        f = plt.figure()
        ax = plt.gca()
        self.buffer_gdf.boundary.plot(ax=ax)
        self.coordinates_gdf.plot(marker='o', color='red', ax=ax)

    def set_gdf(self, gdf_data):
        self.gdf = gdf_data

    def get_gdf(self):
        return self.gdf

    def set_loc_gdf(self):
        assert self.gdf is not None
        for index, row in self.gdf.iterrows():
            if row.geometry.contains(self.coordinates):
                self.loc_gdf = self.gdf.loc[[index]]

    def get_loc_gdf(self):
        return self.loc_gdf

    def set_neighborhoods(self):
        assert self.gdf is not None
        assert self.buffer is not None
        ring = self.buffer
        ring_area = self.buffer.area
        selection = []
        selection_intersect = []
        selection_overlap = []
        for index, row in self.gdf.iterrows():
            if ring.intersects(row.geometry):
                intersecting_area = ring.intersection(row.geometry).area
                overlapping_area = row.geometry.intersection(ring).area
                overlapping_coverage = overlapping_area / row.geometry.area
                intersection_coverage = intersecting_area / ring_area
                selection.append(index)
                selection_intersect.append(intersection_coverage)
                selection_overlap.append(overlapping_coverage)


        self.neighborhoods_gdf = self.gdf.loc[selection]
        self.neighborhoods_gdf['intersection'] = selection_intersect
        self.neighborhoods_gdf['overlap'] = selection_overlap


    def get_neighborhoods(self):
        return self.neighborhoods_gdf

    def plot_neighborhoods(self):
        assert self.neighborhoods_gdf is not None
        f = plt.figure(figsize=(8, 8))
        ax = plt.gca()
        self.buffer_gdf.boundary.plot(ax=ax, color='blue')
        self.coordinates_gdf.plot(marker='o', color='red', ax=ax)
        self.neighborhoods_gdf.boundary.plot(ax=ax, color='black')
        plt.show()
