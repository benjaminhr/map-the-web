import requests
import re
import sys
import urllib.parse
import bs4
import validators
import queue 
from treelib import Node, Tree
from threading import Lock, Thread

class Search:
  lock = None
  depth = 1
  visited_urls = None
  urls_to_visit = None

  def start(self, start_url, depth):
    self.lock = Lock()
    self.depth = depth
    self.visited_urls = Tree()
    self.urls_to_visit = queue.Queue()

    initial_url = self.validate_url(start_url)
    self.run(initial_url, initial=True)
    
    threads = []
    for i in range(0, 10):
      thread = Thread(target=self.loop)
      threads.append(thread)
      threads[i].start()

    for thread in threads:
      thread.join()

    return self.visited_urls.to_json()

  def run(self, url, initial=False):
    urls_to_visit = self.urls_to_visit
    visited_urls = self.visited_urls

    if initial:
      url = {
        "url": url,
        "source": url
      }

    html = self.get_html(url["url"])

    if html != "failed":
      links = self.get_links(html, url["url"])
      
      self.lock.acquire()
      for link in links:
        self.urls_to_visit.put({ 
          "url": link, 
          "source": url["url"]
        }) 

      if not self.visited_urls.contains(url["url"]):  
        visited_urls.create_node(
          url["url"], # name
          url["url"], # value
          parent=None if initial else url["source"] # root or parent
        )
      self.lock.release()

  def loop(self):
    while not self.urls_to_visit.empty():
      # stop execution, and return json tree
      if self.visited_urls.depth() == self.depth + 1:
        break

      url = self.urls_to_visit.get()
      self.run(url)

  def validate_url(self, url):
    if not validators.url(url):
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
      print(e)
      return 'failed'
        
  def get_links(self, html, parent):
    soup = bs4.BeautifulSoup(html, features="html.parser")
    links = []
  
    for link in soup.findAll('a', href=True):
      link = link["href"]
      if not validators.url(link):
        continue 

      stripped_link = self.remove_queryparams(link) 
    
      if stripped_link[0] == '#' or stripped_link == '/':
        continue

      # if url in form '/blog'
      if stripped_link[0] == '/':
        if parent[-1] == '/':
          # remove extra /
          stripped_link = parent + stripped_link[1:]
        
        stripped_link = parent + stripped_link

      validated_url = self.validate_url(stripped_link)
      links.append(validated_url)

    return links

  def remove_queryparams(self, url):
    return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)    

        