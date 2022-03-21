import re
import data_model
from api_functions import check_for_palm, create_palm_products, search_payload

def api_results(searched_item):

    foods, result = search_payload(searched_item)

    p = re.compile(r'([^,]*PALM[^,]*),')
    pp = re.compile(r'([^,]*TOCOPHER[^,]*),')
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
        if branded_food_category is None:
            branded_food_catergory = ""

        ingredients_string = result['foods'][i].get('ingredients').upper().strip(".")
        ingredients = ingredients_string.split(", ")
        
        palm_ingredients = []
        palm_names = p.findall(ingredients_string)
        possible_palm_names = pp.findall(ingredients_string)
        palm_list = data_model.PalmAlias.query.all()
        contains_palm, palm_ingredients = check_for_palm(palm_names, palm_ingredients, palm_list, ingredients)
        product = data_model.Product.query.filter(data_model.Product.fdc_id == fdc_id).first()

        if product is None:
            product = data_model.create_product(name, descriptor, contains_palm, fdc_id, ingredients, brand)
            data_model.db.session.add(product)
            data_model.db.session.commit()
        if contains_palm == "Doesn't contain palm oil":
            palm_ingredients = []
            palm_list = data_model.PossiblePalm.query.all()
            palm_names = pp.findall(ingredients_string)
            contains_palm, palm_ingredients = check_for_palm(palm_names, palm_ingredients, palm_list, ingredients)
            if contains_palm == "Doesn't contain palm oil":
                a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients, "product_id": product.id}
            elif contains_palm == "THIS PRODUCT CONTAINS PALM OIL":
                contains_palm = "This product has ingredients that may be derived from Palm Oil"
                a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients, "product_id": product.id, "Palm_ingredients": palm_ingredients, "branded_food_category": branded_food_category}
        elif contains_palm == "THIS PRODUCT CONTAINS PALM OIL":
            alias_description = create_palm_products(palm_ingredients, product)
            palm_ingredients = set(palm_ingredients)
            a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients, "Palm_ingredients": palm_ingredients, "Alias_description": alias_description, "branded_food_category": branded_food_category, "product_id": product.id}

        all_results.append(a_result)
        
    return all_results
