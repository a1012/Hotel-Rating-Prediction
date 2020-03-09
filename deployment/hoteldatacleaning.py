import os, json
import pandas as pd
import csv
from pandas.io.json import json_normalize
import re
import csv

# this finds our json files
path_to_json = 'C:/Users/ayu_a/Downloads/json/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
#print(json_files[0])
def validate_json_keys(json):
    if 'Name' not in json.keys():
        print("key : Name is not present")
        return False
    if 'Price' not in json.keys():
        print("key : Price is not present")
        return False
    if 'Address' not in json.keys():
        print("key : Price is not present")
        return False
    
    return True

# we need both the json and an index number so use enumerate()
name =[]
price = []
address=[]
reviews=[]
authors=[]
a_location =[]
Content=[]
title=[]


for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)
        hotelname=json_text["HotelInfo"]

        if validate_json_keys(hotelname):
            
            hotel_name = hotelname['Name']
            prices =hotelname['Price']
            hotel_address = hotelname['Address']
            hotel_address = re.sub('<[^>]*>',"",hotel_address.rstrip().lstrip())
            
            review_list = json_text["Reviews"]
            for review in review_list:
                name.append(hotel_name)
                price.append(prices)
                address.append(hotel_address)
                reviews.append(review['Ratings'])
                authors.append(review['Author'])
                a_location.append(review['AuthorLocation'] )
                Content.append(review['Content'])
                title.append(review['Title']) 
                #: print(f'Author: {review["Author"]}')
            
        else:
            print(">>Error in JSON data text.\n",)
        
#         for key in json_text["HotelInfo"].keys():            
#             print(">> {0} - {1}".format(key, hotelname[key]))
# print(json_text) 

temp={"HotelName":name,"HotelPrice":price,"HotelAddress":address,"HotelRatings":reviews,"AuthorName":authors,
     "Authorlocation":a_location,"Review":Content,"title":title}

df = pd.DataFrame.from_dict(temp)
df.info()
#Converting dataframe to csv format
df.to_csv('cleaned.csv')