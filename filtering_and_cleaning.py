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

print(excluded_no)


# Write column headers and export data into csv
with open('uni_people.csv', 'w') as csvfile:
    csvfile.write('Title, Birthyear, Nationality, Occuption, Field, Alma mater,  University,  College,  Education, Known for, Filtered typelabel\n')
    fieldnames = ['title', 'ontology/birthYear', 'ontology/nationality_label', 'ontology/occupation_label', 'ontology/field_label', 'ontology/almaMater_label', 'ontology/university_label', 'ontology/college_label', 'ontology/education_label', 'ontology/knownFor_label', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label',]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    for person in people_uni_in_total:
        writer.writerow(person)

