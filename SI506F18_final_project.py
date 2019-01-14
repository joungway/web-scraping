import json
import csv
import requests

# set up cache file name
CACHE_FNAME = "cache_final_data.json"

# your API key (program will not run unless you fill in this)
NYT_API_KEY = "61f2070ed6f74b84bf2342a8227ed464" #from email
GUARDIAN_API_KEY = "af2e1c24-f4c0-4cc7-bbc1-8bbbbde0ce84" # from email

# see if cache file already exist,
## if so, convert the json string into a python dictionary
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_diction = json.loads(cache_contents)
    cache_file.close()

# if not, create an empty cache dictionary to cache data later
except:
    cache_diction = {}


# function to create unique url identifier
def params_unique_combination(baseurl, params_d, private_keys=["api-key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


# function to get data from caching, or make new API call to NYT
## and save response in cache file
def get_from_nyt_caching(search_query):
    baseurl = "https://api.nytimes.com/svc/search/v2/articlesearch.json" # this is for the content endpoint
    params_diction = {}
    params_diction["api_key"] = NYT_API_KEY
    params_diction["q"] = search_query
    params_diction["fq"] = 'source:("The New York Times")'

    unique_ident = params_unique_combination(baseurl,params_d = params_diction)

    if unique_ident in cache_diction:
        print ("getting data from cache file...")
        return cache_diction[unique_ident]
    else:
        print ("making new API call...")
        resp = requests.get(baseurl, params=params_diction)
        cache_diction[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_diction, indent=4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return cache_diction[unique_ident]

#nyt_result = get_from_nyt_caching("fish")
#print(nyt_result)

# function to get data from caching, or make new API call to NYT
## and save response in cache file
def get_from_gua_caching(search_query):
    baseurl = "https://content.guardianapis.com/search" # this is for the content endpoint
    params_diction = {}
    params_diction["api-key"] = GUARDIAN_API_KEY
    params_diction["q"] = search_query
    params_diction["format"]="json"
    params_diction["show-fields"]= "all"

    unique_ident = params_unique_combination(baseurl,params_diction)

    if unique_ident in cache_diction:
        print ("getting data from cache file...")
        return cache_diction[unique_ident]
    else:
        print ("making new API call...")
        resp = requests.get(baseurl, params=params_diction)
        cache_diction[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(cache_diction, indent=4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return cache_diction[unique_ident]

#gua_result = get_from_gua_caching("fish")
#print(gua_result)

class NYTArticle(object):
    def __init__(self, nyt_diction):
        self.article_title =nyt_diction["headline"]["main"]
        self.author = nyt_diction["byline"]["person"][0]["firstname"]+" "+nyt_diction["byline"]["person"][0]["lastname"]

        self.date = nyt_diction["pub_date"]
        self.word_count = nyt_diction["word_count"]
        self.source = nyt_diction["source"]
        if nyt_diction["news_desk"]:
            self.subject=nyt_diction["news_desk"]
        else:
            self.subject= "Unknown"

    def most_common_letter(self):
        clean = self.article_title.replace(" ","").replace("\n","")
        letter_count = {}
        for letter in clean:
            if letter not in letter_count:
                letter_count[letter] = 0
            letter_count[letter] += 1

        char_key = list(letter_count.keys())
        most_common = char_key[0]

        for element in letter_count:
            if letter_count[element] > letter_count[most_common]:
                most_common = element

        return most_common


    def __str__(self):
        nyt_string = "{} was publiched on {} by {}. The author is {}. The subject is {}. It has {} words and the most common letter is {}.".format(self.article_title,self.date,self.source,self.author, self.subject(),self.words_count,self.most_common_letter())
        return nty_string


class GuardianArticle(object):
    def __init__(self, gua_diction):
        self.article_title =gua_diction["webTitle"]
        if gua_diction["fields"]["byline"]:
            self.author=gua_diction["fields"]["byline"]
        else:
            self.author= "Unknown"
        self.date = gua_diction["webPublicationDate"]
        self.word_count = gua_diction["fields"]["wordcount"]
        self.source = gua_diction["fields"]["publication"]
        self.section = gua_diction["sectionName"]

    def most_common_letter(self):
        clean = self.article_title.replace(" ","").replace("\n","")
        letter_count = {}
        for letter in clean:
            if letter not in letter_count:
                letter_count[letter] = 0
            letter_count[letter] += 1
        #print(letter_count)
        char_key = list(letter_count.keys())
        most_common = char_key[0]

        for element in letter_count:
            if letter_count[element] > letter_count[most_common]:
                most_common = element

        return most_common

    def __str__(self):
        gua_string = "{} was publiched on {} by {}. The author is {}. The subject is {}. It has {} words and the most common letter is {}.".format(self.article_title,self.date,self.source,self.author, self.section,self.words_count,self.most_common_letter())
        return gua_string

#test the class
# st = open("cache_final_data.json")
# one_nyt_article = json.loads(st.read())
# st.close()
#
# nyt_articles = NYTArticle(one_nyt_article)
# print(nyt_articles.article_title, "article title")
# print(nyt_articles.date, "date")
# print(nyt_articles.subject, "subject")
# print(nyt_articles.source, "source")
# print(nyt_articles.most_common_letter(), "most common letter")
# print(nyt_articles)
#
# gua_articles = GuardianArticle(one_gua_article)
# print(gua_articles.article_title, "article title")
# print(gua_articles.date, "date")
# print(gua_articles.section, "section")
# print(gua_articles.source, "source")
# print(gua_articles.most_common_letter(), "most common letter")
# print(gua_articles)


nyt = get_from_nyt_caching("fish")
nyt_docs = nyt["response"]["docs"]
nyt_insts=[]
for item in nyt_docs:
    if item["document_type"] =="article":
        nyt_instance = NYTArticle(item)
        nyt_insts.append(nyt_instance)


gua = get_from_gua_caching("fish")
gua_results =gua["response"]["results"]
gua_insts=[]
for item in gua_results:
    if "byline" in item["fields"].keys():
        gua_instance = GuardianArticle(item)
        gua_insts.append(gua_instance)


data = []
for instance in nyt_insts:
    temp = []
    temp.append(instance.article_title)
    temp.append(instance.author)
    temp.append(instance.date)
    temp.append(instance.subject)
    temp.append(instance.word_count)
    temp.append(instance.source)
    temp.append(instance.most_common_letter())
    data.append(temp)
for instance in gua_insts:
    temp = []
    temp.append(instance.article_title)
    temp.append(instance.author)
    temp.append(instance.date)
    temp.append(instance.section)
    temp.append(instance.word_count)
    temp.append(instance.source)
    temp.append(instance.most_common_letter())
    data.append(temp)

csv_file = open("article_info.csv","w")
writer = csv.writer(csv_file, delimiter = ",")
headers_line = ["Article Title","Author","Date","Subject/Section","Words Count","Source","Most Common Letter"]
writer.writerow(headers_line)

for row in data:
    writer.writerow(row)
# for row_nyt in data_nyt:
#     writer.writerow(row_nyt)
# for row_gua in data_gua:
#     writer.writerow(row_gua)


csv_file.close()
