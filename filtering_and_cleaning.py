import json
import csv

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
    
    people_all_total += people_all
    excluded_total += excluded
    people_total += people
    people_uni_total += people_uni


# Write column headers and export data into csv
with open('uni_people.csv', 'w') as csvfile:
    csvfile.write('Title, Birthyear, Nationality, Occuption, Field, Alma mater,  University,  College,  Education, Known for, full typelabel, description\n')
    fieldnames = ['title', 'ontology/birthYear', 'ontology/nationality_label', 'ontology/occupation_label', 'ontology/field_label', 'ontology/almaMater_label', 'ontology/university_label', 'ontology/college_label', 'ontology/education_label', 'ontology/knownFor_label', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label', '"http://purl.org/dc/elements/1.1/description"']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    for person in people_uni_total:
        writer.writerow(person)

