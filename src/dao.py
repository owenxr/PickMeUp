import requests
import json
from pexels_api import API
import math
from db import Category, Data

###
###     Data Retrieval Methods
###

def retrive_data(categories, pexels_key):
    #num_requests_each = math.floor(190/len(categories))

    api = API(pexels_key)

    data = []

    for c in categories:
        api.search(c, page=1, results_per_page=3)
        photos = api.get_entries()

        for photo in photos:

            img = photo.url
            photographer = photo.photographer

            img = img[:len(img)-1].split('-')
            img = img[len(img)-1]

            url = "https://images.pexels.com/photos/" + img + "/pexels-photo-" + img + ".jpeg"

            dat = {
                'category': c,
                'photo': url,
                'photographer': photographer
            }

            data.append(dat)

    return data

def get_quote(search_ind, quotes_key, quotes_host):

    headers = {
    'x-rapidapi-key': quotes_key,
    'x-rapidapi-host': quotes_host
    }

    url = "https://yusufnb-quotes-v1.p.rapidapi.com/widget/~" + search_ind + ".json"
    response = requests.request("GET", url, headers=headers)
    body = json.loads(response.text)
    
    quote = body.get('quote')
    author = body.get('by')

    return {
        'category': search_ind,
        'quote': quote,
        'author': author
    }
        