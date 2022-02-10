import requests
import re
import data_model
from api_functions import check_for_palm, create_palm_products
import json

def api_alternatives():
    payload = {"includeDataTypes":
                {"Branded": True},
                "referenceFoodsCheckBox": True,
                "requireAllWords": True,
                "sortCriteria":{"sortColumn":"description","sortDirection":"asc"},
                "pageNumber": 1,
                "exactBrandOwner": None,
                "currentPage":1,
                "generalSearchInput":"Processed Cereal Products",
                "includeMarketCountries":{"United States": True,"Canada":True,"New Zealand": True},
                "sortField":"",
                "sortDirection": None}

    payload = json.dumps(payload)
    # payload ='{"includeDataTypes":{"Branded":true},"referenceFoodsCheckBox":true,"requireAllWords":true,"sortCriteria":{"sortColumn":"description","sortDirection":"asc"},"pageNumber":1,"exactBrandOwner":null,"currentPage":1,"generalSearchInput":"Processed Cereal Products","includeMarketCountries":{"United States":true,"Canada":true,"New Zealand":true},"sortField":"","sortDirection":null}'

# POST /portal-data/external/search HTTP/1.1
# Host: fdc.nal.usda.gov
# Connection: keep-alive
# Content-Length: 375
# sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"
# Accept: application/json, text/plain, */*
# Content-Type: application/json
# sec-ch-ua-mobile: ?0
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36
# sec-ch-ua-platform: "Windows"
# Origin: https://fdc.nal.usda.gov
# Sec-Fetch-Site: same-origin
# Sec-Fetch-Mode: cors
# Sec-Fetch-Dest: empty
# Referer: https://fdc.nal.usda.gov/fdc-app.html
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-US,en;q=0.9
# Cookie: _ga=GA1.4.612171128.1635652223; _ga=GA1.2.612171128.1635652223; nmstat=1681bba0-a875-cb03-46a8-f7fa867c0069; _gid=GA1.4.918514319.1644362397; _gid=GA1.2.918514319.1644362397; ak_bmsc=2350E47C000AE116E87EF94A9A512E92~000000000000000000000000000000~YAAQNWAZuCaRCtZ+AQAAubYY3Q7+Qhyrjz73CBsqRnU2bFVDb3oVANDUF7WKSdLH7R3lLYreuGLyTDzqHpcnLf1XK+8/4+8gKCUoVEV5WCWgST8AZig4Feh/ozNf3p3uSMsjZWKdHpaQvOsMUqON/r0+YQjAghqPrun8IfRQzbUTdRUceM8E5t3cNN+jcI9Lp7EfjZKl1dRrUA/ZtKaacAM9Op+bG4C3AsK21n5W2olBgMd6vTvmjkkQcBJG+7WuBlx0VpOYGxymCvT502owQ9rboYqAI5mwqV7TKeWletl4HKUqgyrbHBeEcr2tRtiX3dso1eWonBaltaHqKJgjK4pk9uzb+Mes2EXo8heeSFj67JYYW3wr+oDzY5l3bzITtZs9tQbgXjuE


    search = requests.post('https://fdc.nal.usda.gov/portal-data/external/search', data = payload, headers={"Content-Type": "application/json"})
    result = search.json()
    print(result)
    p = re.compile(r'([^,]*PALM[^,]*),')

    # foods = result['foods']
    # print(foods)
    all_alternatives = []

api_alternatives()
    # for i in range(len(foods)):
    #     food_category = result['foods'][i].get('foodCategory')
    #     # if food_category == branded_food_category:

    #     name = result['foods'][i].get('brandName')
    #     if name is None:
    #         name = ""
    #     name = name.title()

    #     descriptor = result['foods'][i].get('description')
    #     if descriptor is None:
    #         descriptor = ""
    #     descriptor = descriptor.title()

    #     fdc_id = result['foods'][i].get('fdcId')

    #     brand = result['foods'][i].get('brandOwner')
    #     if brand is None:
    #         brand = ""
    #     brand = brand.title()

    #     ingredients_string = result['foods'][i].get('ingredients').upper()
    #     ingredients = ingredients_string.split(", ")
        
    #     palm_ingredients = []
    #     palm_names = p.findall(ingredients_string)
    #     palm_list = data_model.PalmAlias.query.all()
    #     contains_palm = check_for_palm(palm_names, palm_ingredients, palm_list, ingredients)

    #     new_product = data_model.create_product(name, descriptor, contains_palm, fdc_id, ingredients, brand)
    #     data_model.db.session.add(new_product)
    #     data_model.db.session.commit()

    #     if contains_palm is False:
    #         palm_ingredients = ""
    #         alt_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients}
    #         all_alternatives.append(alt_result)
    #     elif contains_palm is True:
    #         alias_description = create_palm_products(palm_ingredients, new_product)
            
    # return all_alternatives

