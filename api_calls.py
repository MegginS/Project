import requests
import re
import data_model
from api_functions import check_for_palm, create_palm_products

def api_results(searched_item):
    payload = {
                'query': searched_item,
                'dataType': 'Branded',
                'pageSize': '5',
                'api_key': 'fJ2wh3xW6pxbmvirGjlwGhs2gwTaXedDlqxrXofR'
                }

    search = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', params = payload)
    result = search.json()

    p = re.compile(r'([^,]*PALM[^,]*),')

    foods = result['foods']
    all_results = []

    for i in range(len(foods)):

        name = result['foods'][i].get('brandName')
        if name is None:
            name = ""
        name = name.title()

        descriptor = result['foods'][i].get('description')
        if descriptor is None:
            descriptor = ""
        descriptor = descriptor.title()

        fdc_id = result['foods'][i].get('fdcId')

        brand = result['foods'][i].get('brandOwner')
        if brand is None:
            brand = ""
        brand = brand.title()

        branded_food_category = result['foods'][i].get('foodCategory')

        ingredients_string = result['foods'][i].get('ingredients').upper()
        ingredients = ingredients_string.split(", ")
        
        palm_ingredients = []
        palm_names = p.findall(ingredients_string)
        palm_list = data_model.PalmAlias.query.all()
        contains_palm = check_for_palm(palm_names, palm_ingredients, palm_list, ingredients)

        new_product = data_model.create_product(name, descriptor, contains_palm, fdc_id, ingredients, brand)
        data_model.db.session.add(new_product)
        data_model.db.session.commit()

        if contains_palm is False:
            palm_ingredients = ""
            a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients}
        elif contains_palm is True:
            alias_description = create_palm_products(palm_ingredients, new_product)
            palm_ingredients = set(palm_ingredients)
            a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients, "Palm_ingredients": palm_ingredients, "Alias_description": alias_description, "branded_food_category": branded_food_category}
        
        all_results.append(a_result)
        
    return all_results

 # ingredients and change boolean for comtains palm- yes, no -possibly