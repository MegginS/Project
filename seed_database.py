import os
import json

import flask_app
import data_model

os.system("dropdb palm")
os.system('createdb palm')

data_model.connect_to_db(flask_app.app)
data_model.db.create_all()

with open('data/aliases.json') as f:
    alias_data = json.loads(f.read())

aliases_in_db = []
for alias in alias_data:

    alias_name = alias["alias_name"]
    description = alias["description"]

    created_alias = data_model.create_alias(alias_name, description)
    aliases_in_db.append(created_alias)

data_model.db.session.add_all(aliases_in_db)
data_model.db.session.commit()


# pg_dump db_name > file.sql