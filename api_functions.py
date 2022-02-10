import data_model

def check_for_palm(palm_names, palm_ingredients, palm_list, ingredients):
        contains_palm = False

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

        return contains_palm
        
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

