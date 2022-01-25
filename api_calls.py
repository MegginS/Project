import requests
import re
from model import db, Product, Product_with_palm, create_product, create_product_with_palm, connect_to_db

payload = {
            'query': 'nutella',
            'dataType': 'Branded',
            'brandOwner': '',
            'pageSize': '2',
            'api_key': 'fJ2wh3xW6pxbmvirGjlwGhs2gwTaXedDlqxrXofR'
            }

search = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', params = payload)
result = search.json()

palm_aliases = ["Palm Oil", "Palm Kernel", "Palm Kernel Oil", "Palm Fruit Oil", "Palmate, Palmitate", "Palm olein", "Glyceryl Stearate", 
                "Stearic Acid", "Elaeis Guineensis", "Palmitic Acid", "Palm Stearine", "Palmitoyl Oxostearamide", 
                "Palmitoyl Tetrapeptide", "Sodium Laureth Sulfate", "Sodium Lauryl Sulfate", "Sodium Kernelate",
                "Sodium Palm Kernelate", "Sodium Lauryl Lactylate", "Sulphate", "Hydrated Palm Glycerides", "Etyl Palmitate", 
                "Octyl Palmitate", "Palmityl Alcohol", "palm"]

p = re.compile(r'([^,]*PALM[^,]*),')


foods = result['foods']

for i in range(len(foods)):
    name = result['foods'][i].get('brandName')
    descriptor = result['foods'][i].get('description')
    fdc_id = result['foods'][i].get('fdcId')
    brand = result['foods'][i].get('brandOwner')
    ingredients_string = result['foods'][i].get('ingredients')
    ingredients = ingredients_string.split(", ")
    contains_palm = False
    palm_ingredients = []
    palm_names = p.findall(ingredients_string)
    if palm_names != []:
        contains_palm = True
        for palm_name in palm_names:
            palm_name = palm_name.strip(" ")
            palm_ingredients.append(palm_name)
    for palm_alias in palm_aliases:
        if palm_alias.upper() in ingredients:
            contains_palm = True
            if palm_alias.upper() not in palm_ingredients:
                palm_ingredients.append(palm_alias.upper())
    new_product = create_product(name, contains_palm, fdc_id, ingredients, brand)
    db.session.add(new_product)
    db.session.commit()
    if contains_palm is True:
        new_palm_product = create_product_with_palm(new_product.id, alias.id)
# need to define alias id
        db.session.add(new_palm_product)
        db.session.commit()





print(name, descriptor, fdc_id, brand, contains_palm, ingredients, palm_ingredients)
