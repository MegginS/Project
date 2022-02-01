import requests
import re
import data_model


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

    foods = result['foods']

    for i in range(len(foods)):
        name = result['foods'][i].get('brandName').title()
        descriptor = result['foods'][i].get('description').title()
        fdc_id = result['foods'][i].get('fdcId')
        brand = result['foods'][i].get('brandOwner')
        ingredients_string = result['foods'][i].get('ingredients')
        ingredients = ingredients_string.split(", ")
        contains_palm = False
        palm_ingredients = []
        palm_names = p.findall(ingredients_string)
        palm_list = data_model.PalmAlias.query.all()

        if palm_names != []:
            contains_palm = True
            for palm_name in palm_names:
                palm_name = palm_name.strip(" ")
                palm_ingredients.append(palm_name)
        
        for palm_alias in palm_list:
            if palm_alias.alias_name in ingredients:
                contains_palm = True
                if palm_alias.alias_name not in palm_ingredients:
                    palm_ingredients.append(palm_alias.alias_name)
        new_product = data_model.create_product(
                    name,
                    descriptor,
                    contains_palm,
                    fdc_id,
                    ingredients,
                    brand)
        data_model.db.session.add(new_product)
        data_model.db.session.commit()
        if contains_palm is True:
            for palm_ingredient in palm_ingredients:
                alias = data_model.PalmAlias.query.filter(data_model.PalmAlias.alias_name == palm_ingredient).all()
                if alias != []:
                    product_palm = data_model.create_product_with_palm(new_product.id, alias[0].id)
                elif alias == []:
                    other_alias = data_model.PalmAlias.query.filter(data_model.PalmAlias.alias_name == "OTHER PALM OIL INGREDIENT").all()
                    product_palm = data_model.create_product_with_palm(new_product.id, other_alias[0].id)

            data_model.db.session.add(product_palm)
            data_model.db.session.commit()

    
        return {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand Owner": brand, "Contains Palm": contains_palm, "Ingredients": ingredients, "Palm Ingredients": palm_ingredients}