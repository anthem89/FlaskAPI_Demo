from flask import Flask
from flask import request
from test import *
from markupsafe import escape
import json

app = Flask(__name__)

# Test Route
@app.route('/coordinates/', methods=['GET', 'POST'])
def coordinates():
    address = str(escape(request.args.get('address', None).replace("_", " ")))
    
    res = ReturnGeoSpatialData(address)
    ret = json.dumps([res.coordinates_gdf.to_json()])
    return ret

@app.route('/neighborhoods/', methods=['GET', 'POST'])
def neighborhoods():
    address = str(escape(request.args.get('address', None).replace("_", " ")))
    distance = int(escape(request.args.get('distance', None)))
    distanceUnits = str(escape(request.args.get('distanceUnits', None)))
    
    res = ReturnGeoSpatialData(address, distance, distanceUnits)
    ret = json.dumps([res.neighborhoods_gdf.to_json()])
    return ret

    # A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to the GeoSpatial API</h1>"

if __name__ == '__main__':
    # Deployed version
    app.run(threaded=True, port=5000)