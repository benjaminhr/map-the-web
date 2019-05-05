import requests
import re
import sys
import urllib.parse
import bs4
import json     
import validators
from treelib import Node, Tree

class Search:
  visited_urls = None
  urls_to_visit = []
  depth = 1

  def start(self, start_url, depth):
    self.visited_urls = Tree()
    self.urls_to_visit = []
    self.depth = depth

    initial_url = self.validate_url(start_url)
    self.run(initial_url, initial=True)
    return self.loop()

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
      links_dict = [{ 
        "url": link, 
        "source": url["url"]
      } for link in links]

      visited_urls.create_node(
        url["url"], # name
        url["url"], # value
        parent=None if initial else url["source"] # root or parent
      )

      url in urls_to_visit and urls_to_visit.remove(url) 
      urls_to_visit.extend(links_dict)

  def loop(self):
    for url in self.urls_to_visit:
      if self.visited_urls.depth() == self.depth + 1:
        return self.visited_urls.to_json()

      if not self.visited_urls.contains(url["url"]):
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

        