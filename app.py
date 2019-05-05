import os
from flask import Flask, request
from utils.search import Search
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/search', methods=['POST'])
@cross_origin()
def search():
  req_data = request.get_json()

  if 'url' in req_data:
    url = req_data["url"]
    depth = req_data["depth"] if req_data["depth"] else None
    search = Search()
    json = search.start(url, depth)

    return json

  return "You did not specify a url in request body."

if __name__ == "__main__":
  app.run(
    debug=True,
    host='0.0.0.0',
    port=int(os.environ.get('PORT', 8080))
  )