import data_model
from api_functions import check_for_palm, create_palm_products, search_payload, check_re_palm, get_result_value

def api_results(searched_item):

    foods, result = search_payload(searched_item)
    all_results = []

    for i in range(len(foods)):

        name = get_result_value(result['foods'][i].get('brandName'))
        descriptor = get_result_value(result['foods'][i].get('description'))
        fdc_id = result['foods'][i].get('fdcId')
        brand = get_result_value(result['foods'][i].get('brandOwner'))
        branded_food_category = get_result_value(result['foods'][i].get('foodCategory'))
        ingredients_string = result['foods'][i].get('ingredients').upper().strip(".")

        ingredients = ingredients_string.split(", ")
        palm_ingredients = []

        contains_palm, palm_ingredients = check_re_palm(ingredients_string, palm_ingredients)
        palm_list = data_model.PalmAlias.query.all()
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
