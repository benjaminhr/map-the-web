import requests
import re
import sys
import signal
import bs4
import urllib.parse
from threading import RLock, Thread, get_ident

lock = RLock()
visited_urls = []
urls_to_visit = []
max_depth = 200

class Search:
  def start(self, start_url):
    initial_url = self.validate_url(start_url)
    self.run(initial_url, initial=True)
    self.loop()

  def validate_url(self, url):
    if (not url.lower().startswith(('http', 'https'))):
      return 'https://' + url
    return url
  
  def get_html(self, url):
    try:
      resp = requests.get(url)
      req_time = resp.elapsed.total_seconds()
      html = resp.text

      print("FROM: " + str(get_ident()))
      print(url + ": " + str(req_time))
      return html    
    except Exception as e:
      return 'failed'
        
  def get_links(self, html, parent):
    soup = bs4.BeautifulSoup(html, features="html.parser")
    links = []
  
    for link in soup.findAll('a', href=True):
      stripped_link = self.remove_queryparams(link.get('href')) 
      
      if (stripped_link == '#'):
        continue

      # if url in form '/blog'
      if len(stripped_link) >= 1 and stripped_link[0] == '/':
        if parent[-1] == '/':
          stripped_link = parent + stripped_link[1:]
        
        stripped_link = parent + stripped_link

      validated_url = self.validate_url(stripped_link)
      links.append(validated_url)

    return links

  def remove_queryparams(self, url):
    return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)
  
  def run(self, url, initial=False):
    global urls_to_visit
    global visited_urls

    if initial:
      url = {
        "url": url,
        "source": url
      }

    html = self.get_html(url["url"])

    if html != "failed":
      links = self.get_links(html, url["source"])
      links_dict = [{ 
        "url": link, 
        "source": link
      } for link in links]

      lock.acquire()  
      visited_urls.append(url)
      url in urls_to_visit and urls_to_visit.remove(url) 
      urls_to_visit.extend(links_dict)
      lock.release()

  def loop(self):
    global urls_to_visit
    global visited_urls
    global max_depth

    for url in urls_to_visit:
      if url not in visited_urls and max_depth > 0:
        self.run(url)
        max_depth -= 1

urls = [
  "https://google.com",
  "https://fb.com",
  "https://youtube.com",
  "https://apple.com",
  "https://bbc.co.uk",
  "https://repl.it",
  "https://example.com",
  "https://news.ycombinator.com",
]
threads = []
for i in range(0, 8):
  search = Search() 
  thread = Thread(target=search.start, args=(urls[i],))
  threads.append(thread)
  threads[i].start()

for thread in threads:
  thread.join()

# Stop ctrl-c, program quit errors
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))