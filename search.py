import requests
import re
import sys
import signal
import bs4
import urllib.parse

# Stop ctrl-c, program quit errors
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

class Search:
  queue = []
  visited_urls = []

  def start(self, start_url):
    initial_url = self.validate_url(start_url)
    html = self.get_html(initial_url)
    links = self.get_links(html)

    self.queue.extend(links)
    self.run()

  def validate_url(self, url):
    if (not url.lower().startswith(('http', 'https'))):
      return 'https://' + url
    return url
  
  def get_html(self, url):
    try:
      resp = requests.get(url)
      req_time = resp.elapsed.total_seconds()
      html = resp.text

      print(url + ": " + str(req_time))
      return html    
    except Exception as e:
      return 'failed'
        
  def get_links(self, html):
    soup = bs4.BeautifulSoup(html, features="html.parser")
    links = []
  
    for link in soup.findAll('a', href=True):
      stripped_link = self.remove_queryparams(link.get('href')) 
      validated_url = self.validate_url(stripped_link)

      links.append(validated_url)

    return links

  def remove_queryparams(self, url):
    return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)

  def run(self):
    for url in self.queue:
      if url not in self.visited_urls:
        self.visited_urls.append(url) 
        self.queue.remove(url)

        html = self.get_html(url)
        if html != "failed":
          links = self.get_links(html)
          self.queue.extend(links)

initial_url = sys.argv[1]
run1 = Search()
run1.start(initial_url)