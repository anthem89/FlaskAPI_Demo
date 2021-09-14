from flask import Flask
from flask import request
from test import *
from markupsafe import escape
import json

app = Flask(__name__)

# Test Route
@app.route('/test/', methods=['GET', 'POST'])
def test():
    address = str(escape(request.args.get('address', None).replace("_", " ")))
    distance = int(escape(request.args.get('distance', None)))
    distanceUnits = str(escape(request.args.get('distanceUnits', None)))

    res = ReturnGeoSpatialData(address, distance, distanceUnits)
    ret = json.dumps([res.address, res.neighborhoods_gdf.to_json()])
    return ret

    # A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to geospatial-api</h1>"

if __name__ == '__main__':
    # # To Run on local host
    # app.run(host='localhost', port=3000)

    # Deployed version
    app.run(threaded=True, port=5000)