import requests
import re
import data_model
from api_functions import check_for_palm

def api_results(searched_item):
    payload = {
                'query': searched_item,
                'dataType': 'Branded',
                'brandOwner': '',
                'pageSize': '5',
                'api_key': 'fJ2wh3xW6pxbmvirGjlwGhs2gwTaXedDlqxrXofR'
                }

    search = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', params = payload)
    result = search.json()

    p = re.compile(r'([^,]*PALM[^,]*),')
    p2 = re.compile(r'([^,]*PALM OIL[^,]*),')

    foods = result['foods']
    
    all_results = []
    for i in range(len(foods)):
        name = result['foods'][i].get('brandName')
        if name is None:
            name = ""
        name = name.title()
        descriptor = result['foods'][i].get('description').title()
        if descriptor is None:
            descriptor = ""
        descriptor = descriptor.title()
        fdc_id = result['foods'][i].get('fdcId')
        brand = result['foods'][i].get('brandOwner')
        if brand is None:
            brand = ""
        brand = brand.title()
        ingredients_string = result['foods'][i].get('ingredients').upper()
        ingredients = ingredients_string.split(", ")
        alias_description = ""
        # need to make none for all items- ingredients and change boolean for comtains palm- yes, no -possibly
        palm_ingredients = []
        palm_names = p.findall(ingredients_string)
        palm_list = data_model.PalmAlias.query.all()
        contains_palm = check_for_palm(palm_names, palm_ingredients, palm_list, ingredients)

        new_product = data_model.create_product(name, descriptor, contains_palm, fdc_id, ingredients, brand)
        data_model.db.session.add(new_product)
        data_model.db.session.commit()

        if contains_palm is True:
            for palm_ingredient in palm_ingredients:
                alias = data_model.PalmAlias.query.filter(
                    data_model.PalmAlias.alias_name == palm_ingredient).all()
                alias_description = []
                if alias != []:
                    for an_alias in alias:
                        product_palm = data_model.create_product_with_palm(new_product.id, an_alias.id)
                        # alias_description.append(an_alias.description)
                elif alias == []:
                    other_alias = data_model.PalmAlias.query.filter(
                        data_model.PalmAlias.alias_name == "OTHER PALM OIL INGREDIENT").all()
                    product_palm = data_model.create_product_with_palm(new_product.id, other_alias[0].id)
                    # alias_description.append(other_alias[0].description)
                
            data_model.db.session.add(product_palm)
            data_model.db.session.commit()

        if contains_palm is False:
            palm_ingredients = ""
            a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients}
        elif contains_palm is True:
            palm_ingredients = set(palm_ingredients)
            a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients, "Palm_ingredients": palm_ingredients, "Alias_description": alias_description}
        
        all_results.append(a_result)
        
    return all_results