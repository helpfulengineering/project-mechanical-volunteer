import flask
from flask import request, jsonify
import requests
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
  return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/locations', methods=['GET'])
@cross_origin()
def locations():
  lat = 0.0
  lng = 0.0
  rad = .005

  if 'lat' in request.args:
    lat = float(request.args['lat'])

  if 'lng' in request.args:
    lng = float(request.args['lng'])

  if 'rad' in request.args:
    rad = float(request.args['rad'])

  nw_point = {'lng': lng - rad, 'lat': lat + rad}
  se_point = {'lng': lng + rad, 'lat': lat - rad}
  print(nw_point)
  print(se_point)

  url = f"https://healthsites.io/api/v2/facilities/?api-key={api_key}&page=1&extent={nw_point['lng']},{se_point['lat']},{se_point['lng']},{nw_point['lat']}"

  response = requests.get(url)  

  print(response.json())

  return jsonify(response.json())

app.run()