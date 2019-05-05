# map-the-web

To get started:
  - `source bin/active`
  - `flask run`

Endpoints
  - POST `localhost:5000/search` with body: `{ url: "google.com", "depth": <optional> | <any int> }`
  - Returns JSON tree 

Note: Some websites will not work if page links are not valid urls such as wikipedia where urls are in the format `//en.wikipedia.org`. 

