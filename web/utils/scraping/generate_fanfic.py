from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import openai
import json
import re
import os
import time
import sys
import re

#tips: 
#is there always an author for every fanfic? 
#can you use ao3's built in filters to get fanfic that's most relevant to you? 
# what if a fanfic doens't have text (some people post fanart on ao3 instead of fanfiction)? 
#reccomend that they explore the fanficiton website but give tips in case they're busy 
#if .find / .find_all can't find anything it returns a None object 

load_dotenv()

ao3_domain = "https://archiveofourown.org"
# openai.api_key = os.getenv("OPENAI_API_KEY") #uncomment whe we start using open ai

# NUM_TRAINING_FANFIC = 10 #can change for testing! 
JSON_PATH = "put path of json here" #TODO: week 2 this is just a good global var to have, please use it 

#a potential helper function for you to use -- also an exmaple of how to open and load jsons! 
# given a fandom <string>, it returns a link <string> for that fandom's fanfics
def get_link(ui_fandom):
    fandoms_json = open(f"{JSON_PATH}/fandoms.json")
    fandoms = json.load(fandoms_json)
    all_fandoms = fandoms["all"]
    fandoms_json.close() 
    for fandom in all_fandoms:
        if fandom["name"] == ui_fandom:
            return fandom["link"]

#TODO: WEEK 2 (OPTIONAL) potential helper function for get_fanfic_info 
# returns true if fanfic card {type beautiful soup} is in the given language <string>, false otherwise
def is_language(fanfic, language):
    return 

#TODO: WEEK 2 Deliberable finish this function ! I have some very loose guide lines for you, feel free to follow them or start from scratch! 
# returns an array of two elements: 1) an array of all the authors whose fanfiction we scraped; 2. specified {number} fanfics (or all fanfic availiable if the total fanfic is less than the number) of word range {min_length}to {max_length}
# in {language} from the given {fandom} in an array of dicts where the dicts are the formatted fanfic traning data 
#hint: how can we use ao3's preexisting filtering system to help us out, and get us some of the fanfic that we want! 
def get_fanfic_info(fandom, number, language, min_length, max_length):
    counter = 0
    fanfics = []
    authors = []

    # Before: https://archiveofourown.org/tags/*h*DRCL%20Midnight%20Children%20(Manga)/works
    # After: https://archiveofourown.org/works?commit=Sort+and+Filter&work_search%5Bsort_column%5D=hits&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=&work_search%5Bwords_to%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=&tag_id=*h*DRCL+Midnight+Children+%28Manga%29
    sort_by = f""
    link = get_link(fandom) + sort_by

    while counter < number and link != "":
        html = requests.get(link)
        soup = BeautifulSoup(html.text, "lxml")

        #some handling for when the site crashes, you can modify this chunk of code to fit into the code you write, or keep as is 
        site_down = soup.find("p", string=re.compile("Retry later"))
        while site_down != None:
            time.sleep(60) #wait 60 then retry 
            html = requests.get(link)
            soup = BeautifulSoup(html.text, "lxml")
            site_down = soup.find("p", string=re.compile("Retry later"))

      
        # check valid author and fanfic/is a fanfic you want to add 
        # more formatting? getting data you want? 
        # formatting training data
        fanfic = soup.select("ol.work.index.group")
        for f in fanfics:
            author = f.select("h4.heading > a")[1].get_text() 

            # Check language and word count; continue to next fanfiction if constraints not met
            lang = f.select("d1.stats > dd.language").get_text()
            num_words = int(f.select("d1.stats > dd.words").get_text())
            if (lang != language) or ((num_words < min_length) or (num_words > max_length)):
                continue
            
            # My fanfic data will have prompts for relationships, characters, and freeforms
            attributes = f.find_all("li")
            fanfic_info = {"prompt": "write a complete, short fan fiction: \nFandom: " + fandom["name"], "completion"}
            for a in attributes:
                classify = a.attrs['class']
                if (classify != "warnings"):
                    tag = "\n" + classify[0].upper() + classify[1:] + " "
                    text = a.find("a").get_text() + " "
                    fanfic_info["prompt"] += tag + text
            
            # Getting fanfic text
            link_to_text = f.select("h4.heading > a")[0].attrs['href']
            html_to_text = requests.get(link_to_text)
            text_soup = BeautifulSoup(html_to_text.text, 'lxml')
            

            # Appending fanfic info
            fanfics.append(fanfic_info)

        next_page = "get next potential page here"
        if next_page != None:
            link = "link for next page"
        else:
            link = ""

    return [authors, fanfics]

#TODO: WEEK 4 (OPTIONAL) potential helper function!
# returns true if FineTuning the model of {model_id} is still running/processing, false once succeeded
def still_running(model_id):
    return 

#TODO: WEEK 4 (OPTIONAL) potential helper function!
# returns full fanfic text <string> given {fanfic_link} <string> 
def get_fanfic(fanfic_link):
    return 

#TODO: WEEK 4(OPTIONAL) potential helper function! 
#creates a new fineTuned model, finetuned on {data}, that will be able to generate new fanfic from the specified {fandom}
#returns the model id once the model is created (make sure you wait unti the model is created before you return the modelid)
def create_fineTuned_model(fandom, data): 
    # converting training data to a jsonl
    # upload jsonl file onto openAI systems 
    # create fineTuned model request 
    # make sure our model is ready to use!
    return 

#TODO: WEEK 4 deliverable 
# given a user inputted {fandom} and an array of {tags}, this function returns a dictionary of the format of a Fanfic obejct: 
# {
#   "title": <string>, 
#   "content": {"name":{fandom}},
#   "fandom": <string>,
#   "kudos": ["list","of","authors"]
# }
# *where content is the fanfic generated by the finetuned model associated with the {fandom}
#tips/things to keep in mind: 
# notice how in the json file there is a models.json folder; you may utilize this to store any necessary info that you may need 
#   so that if you have already created a model for a fandom, you can simply use it and not generate a model each time 
#but if a model for that fandom doesn't exist, it's time to create the new model 
# the fanfic will take a while to generate... how do we make sure we retreive it after we generate it 
# make sure to update models.json to include the new fine tuned model (if you make a new one!)
# before you return the fanfic may consider making slight format modifications 
#   (can include making sure it's not too explicit; making sure it doesn't end mid sentence etc. )
def generate_fanfic(fandom, tags): 
    Fanfic = {}
    return Fanfic

#TODO: change chosen_fandom_title to the fandom you chose! uncomment when we're ready to connect with the webapp!
#when this file is run directly (not imported), program will check for arguments and run generate_fanfic on them 
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         # change to this later
#         # print(json.dumps(generate_fanfic(sys.argv[1], json.loads(sys.argv[2]))))
#         print(
#             json.dumps(
#                 generate_fanfic("chosen_fandom_title", json.loads(sys.argv[2]))
#             )
#         )
#     else:
#         print("usage: generate_fanfic fandom [tags]")
