import requests
import re
import flask_app
import data_model

data_model.connect_to_db(flask_app.app)

payload = {
            'query': 'nutella',
            'dataType': 'Branded',
            'brandOwner': '',
            'pageSize': '2',
            'api_key': 'fJ2wh3xW6pxbmvirGjlwGhs2gwTaXedDlqxrXofR'
            }

search = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', params = payload)
result = search.json()

# palm_aliases = ["Palm Oil", "Palm Kernel", "Palm Kernel Oil", "Palm Fruit Oil", "Palmate, Palmitate", "Palm olein", "Glyceryl Stearate", 
#                 "Stearic Acid", "Elaeis Guineensis", "Palmitic Acid", "Palm Stearine", "Palmitoyl Oxostearamide", 
#                 "Palmitoyl Tetrapeptide", "Sodium Laureth Sulfate", "Sodium Lauryl Sulfate", "Sodium Kernelate",
#                 "Sodium Palm Kernelate", "Sodium Lauryl Lactylate", "Sulphate", "Hydrated Palm Glycerides", "Etyl Palmitate", 
#                 "Octyl Palmitate", "Palmityl Alcohol", "palm"]

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
    
    palm_list = data_model.Palm_alias.query.all()
    for palm_alias in palm_list:
        if palm_alias.alias_name in ingredients:
            contains_palm = True
            if palm_alias.alias_name not in palm_ingredients:
                palm_ingredients.append(palm_alias.alias_name)
    new_product = data_model.create_product(name, contains_palm, fdc_id, ingredients, brand)
    data_model.db.session.add(new_product)
    data_model.db.session.commit()
    if contains_palm is True:
        for palm_ingredient in palm_ingredients:
            alias = data_model.Palm_alias.query.filter(data_model.Palm_alias.alias_name == palm_ingredient).all()
            if alias != []:
                product_palm = data_model.create_product_with_palm(new_product.id, alias[0].id)

        data_model.db.session.add(product_palm)
        data_model.db.session.commit()

print(name, descriptor, fdc_id, brand, contains_palm, ingredients, palm_ingredients)

# add new aliases when one is not database