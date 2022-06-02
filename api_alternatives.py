import requests
import re
import data_model
from api_functions import check_for_palm, create_palm_products, get_result_value, check_re_palm
import json

def api_alternatives(food_category, pagesize = 10):

    payload = {"includeDataTypes":
                {"Branded": True},
                "referenceFoodsCheckBox": True,
                "requireAllWords": True,
                "pageSize": pagesize,
                "generalSearchInput": food_category,
                "sortDirection": None}
    
    payload = json.dumps(payload)

    search = requests.post('https://fdc.nal.usda.gov/portal-data/external/search', data = payload, headers={"Content-Type": "application/json"})
    result = search.json()

    # p = re.compile(r'([^,.]*PALM[^,.$]*)')
    # pp = re.compile(r'([^,.]*TOCOPHER[^,.$]*)')
    foods = result['foods']
    all_alternatives = []

    for i in range(len(foods)):

        food_category = result['foods'][i].get('foodCategory')
        name = get_result_value(result['foods'][i].get('brandName'))
        descriptor = get_result_value(result['foods'][i].get('description'))
        fdc_id = result['foods'][i].get('fdcId')
        brand = get_result_value(result['foods'][i].get('brandOwner'))
        ingredients_string = result['foods'][i].get('ingredients').upper().strip(".")
        ingredients = ingredients_string.split(", ")
        
        palm_ingredients = []
        palm_list = data_model.PalmAlias.query.all()
        contains_palm, palm_ingredients = check_re_palm(ingredients_string, palm_ingredients)
        contains_palm, palm_ingredients = check_for_palm(palm_ingredients, palm_list, ingredients, contains_palm)
        product = data_model.Product.query.filter(data_model.Product.fdc_id == fdc_id).first()

        if product is None:
            product = data_model.create_product(name, descriptor, contains_palm, fdc_id, ingredients, brand)
            data_model.db.session.add(product)
            data_model.db.session.commit()
        if contains_palm == "Doesn't contain palm oil":
            palm_ingredients = []
            palm_list = data_model.PossiblePalm.query.all()
            contains_palm, palm_ingredients = check_for_palm(palm_ingredients, palm_list, ingredients, contains_palm)
            if contains_palm == "Doesn't contain palm oil":
                palm_ingredients = ""
                alt_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients, "product_id": product.id}
                all_alternatives.append(alt_result)
    if len(all_alternatives) == 0:
        all_alternatives = api_alternatives(food_category, pagesize = pagesize + 150)
        if pagesize > 450:
            return all_alternatives
    if len(all_alternatives) > 0:
        return all_alternatives
