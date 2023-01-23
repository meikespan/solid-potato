import json


# Load JSON list of dictionaries
with open('People/A_people.json') as file:
    a_people_all = json.load(file)


a_people_all= []
excluded =[]
a_people = []
a_people_uni = []


#filtering out all non-persons and criminals
for entry in a_people_all:
    is_fictional = any('fictional' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
    is_criminal = any( 'criminal' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
     
    if is_fictional or is_criminal:
        excluded.append(entry)
    else:
        a_people.append(entry)


#filtering for uni education
for entry in a_people:
    is_educated = False
    for key in entry:
        if type(entry[key]) is list:
            if any(('university' in value.lower() or 'college' in value.lower()) for value in entry[key]):
                is_educated = True
        else:
            if 'university' in entry[key].lower() or 'college' in entry[key].lower():
                is_educated = True
       
    if is_educated:
        a_people_uni.append(entry)

print(len(a_people_all))
print(len(excluded))
print(len(a_people))
print(len(a_people_uni))
