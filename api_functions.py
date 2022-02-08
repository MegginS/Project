

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
        


    #     new_product = data_model.create_product(
    #                 name,
    #                 descriptor,
    #                 contains_palm,
    #                 fdc_id,
    #                 ingredients,
    #                 brand)
    #     data_model.db.session.add(new_product)
    #     data_model.db.session.commit()
    #     if contains_palm is True:
    #         for palm_ingredient in palm_ingredients:
    #             alias = data_model.PalmAlias.query.filter(
    #                 data_model.PalmAlias.alias_name == palm_ingredient).all()
    #             if alias != []:
    #                 product_palm = data_model.create_product_with_palm(new_product.id, alias[0].id)
    #                 alias_description = alias[0].description
    #             elif alias == []:
    #                 other_alias = data_model.PalmAlias.query.filter(
    #                     data_model.PalmAlias.alias_name == "OTHER PALM OIL INGREDIENT").all()
    #                 product_palm = data_model.create_product_with_palm(new_product.id, other_alias[0].id)
                
    #         data_model.db.session.add(product_palm)
    #         data_model.db.session.commit()

    #     if contains_palm is False:
    #         palm_ingredients = ""
    #         a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients}
    #     elif contains_palm is True:
    #         palm_ingredients = set(palm_ingredients)
    #         a_result = {"Name": name, "Descriptor": descriptor, "Fdc_id": fdc_id, "Brand_owner": brand, "Contains_palm": contains_palm, "Ingredients": ingredients, "Palm_ingredients": palm_ingredients, "Alias_description": alias_description}
        
    #     all_results.append(a_result)
        
    # return all_results