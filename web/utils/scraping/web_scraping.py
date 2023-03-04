"""
Authors: Phillip Chen, Anna Chung, Trevor Trinh

This will scrape the "archiveofourown" website for fandoms. It takes in an integer input that will filter out fandoms that have less fanfics than the specified number.
"""
# run this python file to update the json's whenever you want :)
from bs4 import BeautifulSoup
import requests
import json
import re
import sys

ao3_domain = "https://archiveofourown.org"
#TODO: what's the fandoms.json path? and also explore the structure! 
JSON_PATH = "../../json/fandoms.json"

#TODO:? a potential helper function, optional to fill out
# returns an array of each cateogory link (on which multiple fandoms are listed)
def generate_category_links():
    return

"""
Returns the webpage html, text, and BeautifulSoup object for a link

params:
  (str) link : the link to the page
ret:
  html : the result of requesting link
  text : the text of the html
  soup : the BeautifulSoup object for the webpage
"""
def gen_soup(link):
  html = requests.get(link)
  text = html.text
  soup = BeautifulSoup(text, 'lxml')
  return html, text, soup

#TODO:? a potential helper function, optional! 
"""
Returns an array of {"name":"fandom_name", "link":"fandom_link"} for all fandoms

params: 
  (soup) fandom_soup : the BeautifulSoup object to scrape
  (int) minimum : the minimum number of fanfics to include that fandom
ret: 
  (dict) res : array of dictionaries of the all fandom names and links
"""
def get_all_fandoms(fandom_soup, minimum):
  all_fandoms_search = fandom_soup.select("ul.fandom p.actions > a")
  names = []
  links = []
  res = []
  name_regex_patt = r".*<a .*>(.*)<\/a>.*"
  count_regex_patt = r"\((\d+)\)"

  # Going to each fandom webpage and adding to names and links
  for fandom in all_fandoms_search:
    link_to_fandom = ao3_domain + fandom.attrs['href']

    # Creating soup object
    fandom_page_html, fandom_page_text, fandom_page_soup = gen_soup(link_to_fandom)

    fandom_page_search = fandom_page_soup.select("ol.alphabet.fandom.index.group ul.tags.index.group li")

    # Searching fandom category page
    for fand in fandom_page_search:
      fand_str = str(fand)

      # Checking if there are enough fanfictions
      try: 
        num = int(re.search(count_regex_patt, fand_str).group(1))
      except AttributeError:
        pass
      if (num < minimum):
        continue

      # Normal processing if passed minimum
      name = re.search(name_regex_patt, fand_str).group(1)
      link = fand.find("a").attrs['href']
      
      names.append(name)
      links.append(ao3_domain + link)

  # Creating Result
  for i in range(len(names)):
    dictionary = {"name":names[i], "link":links[i]}
    res.append(dictionary)

  return res

#TODO:? a potential helper function, optional! 
"""
Returns an array of {"name":"fandom_name", "link":"fandom_link"} for the top most written fandoms in each category

params: 
  (soup) fandom_soup : the BeautifulSoup object to scrape
ret: 
  (dict) res : array of dictionaries of the top fandom names and links
"""
def get_top_fandoms(fandom_soup):
  top_all_fandoms_search = fandom_soup.select("ol.group > li > a")
  names = []
  links = []
  res = []
  name_regex_patt = r"<a .*>(.*)</a>"

  # Getting all top fandoms on homepage of All Fandoms
  for fandom in top_all_fandoms_search:
    name = re.match(name_regex_patt, str(fandom)).group(1)
    link = fandom.attrs['href']
    
    names.append(name)
    links.append(ao3_domain + link)
  
  # Creating Result
  for i in range(len(names)):
    dictionary = {"name":names[i], "link":links[i]}
    res.append(dictionary)

  return res

#TODO: Week One deliverable ! it's to write a function that will populate fandoms.json 
# creates fandoms.json file in the json folder with all fandoms and top fandoms in the listed format: '*shoudln't return anything'
# {
#    "top":[
#       {
#          "name":"topfandom",
#          "link":"link"
#       }
#    ],
#    "all":[
#       {
#          "name":"fandom",
#          "link":"link"
#       }
#    ]
# }
"""
params:
  (int) minimum : the minimum number of fanfic texts to scrape for in all_fandoms
ret: None
"""
def gen_fandom_json(minimum):
  # Getting into the All Fandoms page
  home_html, home_text, home_soup = gen_soup(ao3_domain)
  
  home_search = home_soup.select_one("ul.menu > li > a")
  all_fandoms_link = ao3_domain + home_search.attrs['href']
  
  # Get the Beautiful Soup object for scraping
  fandoms_html, fandoms_text, fandoms_soup = gen_soup(all_fandoms_link)

  # Calling Helper Functions to get array of dicts for json file
  all_fandoms = get_all_fandoms(fandoms_soup, minimum)
  top_fandoms = get_top_fandoms(fandoms_soup)
  

  # Creating JSON input
  fandoms_json_input = {"top":top_fandoms, "all":all_fandoms}
  json_in = json.dumps(fandoms_json_input, indent=4)

  # Writing to JSON file
  with open(JSON_PATH, 'w') as f:
    f.write(json_in)
  
  print("Success!")
  return 

# get_all_fandoms(BeautifulSoup(requests.get("https://archiveofourown.org/media").text, 'lxml'))
gen_fandom_json(int(sys.argv[1])) # <-- uncomment this and run the file to update or create fandoms.json
