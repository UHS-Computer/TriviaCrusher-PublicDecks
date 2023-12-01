import glob
import operator
import json_fix

import json

tableEntries = []

# first, find all .tcjson files
for f in glob.glob('./**/*.tcjson', recursive=True):
    with open(f) as fi:
        jsonString = fi.read()
        # Convert JSON String to Python
        deck = json.loads(jsonString)
        tableEntries.append(
            {
                "name": deck["name"],
                "icon": deck["icon"],
                "id": deck["id"],
                "description": deck["description"],
                "path": f,
                "language": f.split("/")[1],
                "cardCount": deck["cards"].__len__(),
            })

print(tableEntries)
tableEntries.sort(key=operator.itemgetter('name'))

# write overview file
f = open("./overview.json", 'w')
f.write(json.dumps({"foundLanguages": set(
    [tableEntry["language"] for tableEntry in tableEntries]), "decks": tableEntries}, indent=2))
f.close()
