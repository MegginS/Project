import data_model
import requests

with open('api_keys.txt') as f:
    api_key = f.readline().strip()

def search_payload(searched_item):
    payload = {
                'query': searched_item,
                'dataType': 'Branded',
                'pageSize': '10',
                'api_key': api_key
                }

    search = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', params = payload)
    result = search.json()
    foods = result['foods']

    return foods, result


# def check_for_palm(palm_names, palm_ingredients, palm_list, ingredients):
#         contains_palm = False

#         if palm_names != []:
#             contains_palm = True
#             for palm_name in palm_names:
#                 palm_name = palm_name.strip(" ")
#                 palm_ingredients.append(palm_name)

#         for palm_alias in palm_list:
#             if palm_alias.alias_name in ingredients:
#                 contains_palm = True
#                 if palm_alias.alias_name not in palm_ingredients:
#                     palm_ingredients.append(palm_alias.alias_name)

#         return contains_palm
        
def check_for_palm(palm_names, palm_ingredients, palm_list, ingredients):
        contains_palm = "Doesn't contain palm oil"

        if palm_names != []:
            contains_palm = "THIS PRODUCT CONTAINS PALM OIL"
            for palm_name in palm_names:
                palm_name = palm_name.strip(" ")
                palm_ingredients.append(palm_name)

        for palm_alias in palm_list:
            palm_alias_name = palm_alias.alias_name
            if palm_alias_name.upper() in ingredients:
                contains_palm = "THIS PRODUCT CONTAINS PALM OIL"
                if palm_alias.alias_name not in palm_ingredients:
                    palm_ingredients.append(palm_alias.alias_name)

        return contains_palm, palm_ingredients

def create_palm_products(palm_ingredients, new_product):
    alias_description = []

    for palm_ingredient in palm_ingredients:

        alias = data_model.PalmAlias.query.filter(
            data_model.PalmAlias.alias_name == palm_ingredient).all()

        other_alias = data_model.PalmAlias.query.filter(
            data_model.PalmAlias.alias_name == "OTHER PALM OIL INGREDIENT").all()

        if alias != []:
            product_palm = data_model.create_product_with_palm(new_product.id, alias[0].id)
        elif alias == []:
            product_palm = data_model.create_product_with_palm(new_product.id, other_alias[0].id)

        data_model.db.session.add(product_palm)
        data_model.db.session.commit()

        alias_description.append(product_palm.palm_aliases.description)

    return set(alias_description)

