import json
import csv

people_all_total = []
people_uni_in_total = []
people_uni_total = []
excluded_no = 0

for i in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:

    # Load JSON list of dictionaries
    with open(f'People/{i}_people.json') as file:
        people_all = json.load(file)


    
    people_uni = []
    people_uni_in = []

  #filtering for uni education
    for entry in people_all:
        is_educated = False
        for key in entry:
            if type(entry[key]) is list:
                if any(('university' in value.lower() or 'college' in value.lower()) for value in entry[key]):
                    is_educated = True
            else:
                if 'university' in entry[key].lower() or 'college' in entry[key].lower():
                    is_educated = True
        if is_educated:
            entry['http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label'] = [item for item in entry['http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label'] if (item != 'person') and (item != 'Person') and (item != 'agent') and (item != 'owl#Thing') and (not item.startswith('DUL.owl#')) and (not item.startswith('Q'))]
            people_uni.append(entry)



    #filtering out all non-persons and criminals
    for entry in people_uni:
        is_fictional = any('fictional' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
        is_criminal = any( 'criminal' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
        
        if is_fictional or is_criminal:
            excluded_no += 1
        else:
            people_uni_in.append(entry)


    people_all_total += people_all
    people_uni_in_total += people_uni_in
    people_uni_total += people_uni

    #thus, we are left with all non-fictional, non-criminal people that went to uni in our list of dictionaries 'people_uni_in_total'
    occupation_keys = ['ontology/occupation_label','ontology/field_label', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label']

    for entry in people_uni_in_total:
        searcharea = []
        for key in occupation_keys:
            if key in entry:
                if type(entry[key]) is list:
                    searcharea.extend(entry[key])
                else:
                    searcharea.append(entry[key])
        
        is_athlete = False
        is_academic = False
        is_author = False
        is_official = False

        if 'athlete' in searcharea:
            is_athlete = True
        if 'scientist' in searcharea:
            is_academic = True
        if 'writer' in searcharea:
            is_author = True
        if 'office holder' in searcharea:
            is_official = True

        if is_athlete:
            entry['occupational_group'] = 'athlete'
        elif is_academic:
            entry['occupational_group'] = 'academic'
        elif is_author:
            entry['occupational_group'] = 'author'
        elif is_official:
            entry['occupational_group'] = 'office holder'
        else:
            entry['occupational_group'] = 'other'

print('excluded:', excluded_no)
print('number included', len(people_uni_in_total))

# Write column headers and export data into csv
with open('uni_people.csv', 'w') as csvfile:
    csvfile.write('Title, Birthyear, Occupational group\n')
    fieldnames = ['title', 'ontology/birthYear', 'occupational_group']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    for person in people_uni_in_total:
        writer.writerow(person)

