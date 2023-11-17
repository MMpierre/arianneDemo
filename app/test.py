import json
ref = json.load(open("app/data/GEN/transformed_referentielGEN.json","rb"))

appt = dict()
for i,domain in enumerate(ref.keys()):
    for j,family in enumerate(ref[domain]["children"]):
        for k,occupation in enumerate(family["children"]):
            appt[occupation["prefLabel"][0]["@value"]] = str(i)+str(j)+str(k)

print(appt)
