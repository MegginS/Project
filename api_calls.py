import requests


payload = {
            'query': 'Frosted Flakes',
            'dataType': 'Branded',
            'brandOwner': 'Kellogg',
            'pageSize': '15',
            'api_key': 'fJ2wh3xW6pxbmvirGjlwGhs2gwTaXedDlqxrXofR'
            }

search = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search', params = payload)
result = search.json()

palm_aliases = 'PALM'
rspo = ""

foods = result['foods']

for i in range(len(foods)):
    name = result['foods'][i].get('brandName')
    descriptor = result['foods'][i].get('description')
    fdc_id = result['foods'][i].get('fdcId')
    brand = result['foods'][i].get('brandOwner')
    ingredients_string = result['foods'][i].get('ingredients')
    ingredients = ingredients_string.split(", ")
    if palm_aliases in ingredients:
        contains_palm = True
    else:
        contains_palm = False

    print(name, descriptor, fdc_id, brand, contains_palm)

