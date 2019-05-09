import os
from flask import Flask, request
from utils.search import Search
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

users = {
  "benjamin": "robson",
  "karmjit": "10252"
}

@auth.get_password
def get_pw(username):
  if username in users:
    return users.get(username)
  
  return None

@app.route('/search', methods=['POST'])
@cross_origin()
@auth.login_required
def search():
  req_data = request.get_json()

  if 'url' in req_data:
    url = req_data["url"]
    depth = req_data["depth"] if req_data["depth"] else None
    search = Search()
    json = search.start(url, depth)

    return json

  return "You did not specify a url in request body."

@app.route('/ping', methods=['GET'])
def ping():
  return 'pong'

if __name__ == "__main__":
  app.run(
    debug=True,
    port=int(os.environ.get('PORT', 5000)),
    host="0.0.0.0"
  )