# map-the-web

Deployed with Google Cloud Run + Google Cloud Build

To get started:
  - `source bin/active`
  - `flask run --host=0.0.0.0`
  - Alternatively with docker: `docker build -t map-the-web . && docker run -d -p 5000:5000 map-the-web`

Endpoints
  - POST `localhost:5000/search` with body: `{ url: "google.com", "depth": <optional> | <any int> }`
  - Returns JSON tree 

Note: Some websites will not work if page links are not valid urls such as wikipedia where urls are in the format `//en.wikipedia.org`. 

