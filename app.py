from flask import Flask
from flask import request
from test import *
from markupsafe import escape
import json

app = Flask(__name__)

@app.route('/test/', methods=['GET', 'POST'])
def test():
    address = str(escape(request.args.get('address', None).replace("_", " ")))
    distance = int(escape(request.args.get('distance', None)))
    distanceUnits = str(escape(request.args.get('distanceUnits', None)))

    res = ReturnGeoSpatialData(address, distance, distanceUnits)
    ret = json.dumps([res.address, res.neighborhoods_gdf.to_json()])
    return ret

if __name__ == '__main__':
    app.run(host='localhost', port=3000)