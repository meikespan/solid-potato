import json

people_all_total = []
excluded_total = []
people_total = []
people_uni_total = []

for i in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:

    # Load JSON list of dictionaries
    with open(f'People/{i}_people.json') as file:
        people_all = json.load(file)



    excluded =[]
    people = []
    people_uni = []


    #filtering out all non-persons and criminals
    for entry in people_all:
        is_fictional = any('fictional' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
        is_criminal = any( 'criminal' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
        
        if is_fictional or is_criminal:
            excluded.append(entry)
        else:
            people.append(entry)


    #filtering for uni education
    for entry in people:
        is_educated = False
        for key in entry:
            if type(entry[key]) is list:
                if any(('university' in value.lower() or 'college' in value.lower()) for value in entry[key]):
                    is_educated = True
            else:
                if 'university' in entry[key].lower() or 'college' in entry[key].lower():
                    is_educated = True
        if is_educated:
            people_uni.append(entry)

    print(len(people_all))
    print(len(excluded))
    print(len(people))
    print(len(people_uni))

    people_all_total += people_all
    excluded_total += excluded
    people_total += people
    people_uni_total += people_uni


print("total", len(people_all_total))
print("total", len(excluded_total))
print("total", len(people_total))
print("total", len(people_uni_total))