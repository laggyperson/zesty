# run this python file to update the json's whenever you want :)
from bs4 import BeautifulSoup
import requests
import json
import re

ao3_domain = "https://archiveofourown.org"
#TODO: what's the fandoms.json path? and also explore the structure! 
JSON_PATH = "../../json/fandoms.json"

#TODO:? a potential helper function, optional to fill out
# returns an array of each cateogory link (on which multiple fandoms are listed)
def generate_category_links():
    return

#TODO:? a potential helper function, optional! 
# returns an array of {"name":"fandom_name", "link":"fandom_link"} for all fandoms
def get_all_fandoms(fandom_soup):
  all_fandoms_search = fandom_soup.select("ul.fandom p.actions > a")
  names = []
  links = []
  res = []
  name_regex_patt = r"<a .*>(.*)</a>"

  # Going to each fandom webpage and adding to names and links
  for fandom in all_fandoms_search:
    link_to_fandom = ao3_domain + fandom.attrs['href']

    # Creating soup object
    fandom_page_html = requests.get(link_to_fandom)
    fandom_page_text = fandom_page_html.text
    fandom_page_soup = BeautifulSoup(fandom_page_text, 'lxml')

    fandom_page_search = fandom_page_soup.select("ol.fandom ul.group a")
    
    # Searching fandom category page
    for fand in fandom_page_search:
      name = re.match(name_regex_patt, str(fand)).group(1)
      link = fandom.attrs['href']
      
      names.append(name)
      links.append(ao3_domain + link)

  # Creating Result
  for i in range(len(names)):
    dictionary = {"name":names[i], "link":links[i]}
    res.append(dictionary)

  return res

#TODO:? a potential helper function, optional! 
# returns an array of {"name":"fandom_name", "link":"fandom_link"} for the top most written fandoms in each category
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
def gen_fandom_json():
  # Getting into the All Fandoms page
  home_html = requests.get(ao3_domain)
  home_text = home_html.text
  home_soup = BeautifulSoup(home_text, 'lxml')
  
  home_search = home_soup.select_one("ul.menu > li > a")
  all_fandoms_link = ao3_domain + home_search.attrs['href']
  
  # Get the Beautiful Soup object for scraping
  fandoms_html = requests.get(all_fandoms_link)
  fandoms_text = fandoms_html.text
  fandoms_soup = BeautifulSoup(fandoms_text, 'lxml')

  # Calling Helper Functions to get array of dicts for json file
  all_fandoms = get_all_fandoms(fandoms_soup)
  top_fandoms = get_top_fandoms(fandoms_soup)

  # Creating JSON input
  fandoms_json_input = {"top":top_fandoms, "all":all_fandoms}
  json_in = json.dumps(fandoms_json_input, indent=4)

  # Writing to JSON file
  with open(JSON_PATH, 'w') as f:
    f.write(json_in)
  
  return 

# get_all_fandoms(BeautifulSoup(requests.get("https://archiveofourown.org/media").text, 'lxml'))
gen_fandom_json() # <-- uncomment this and run the file to update or create fandoms.json
