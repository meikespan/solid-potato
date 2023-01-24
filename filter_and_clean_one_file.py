import json
import csv


# Load JSON list of dictionaries
with open('People/A_people.json') as file:
    a_people_all = json.load(file)


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
        entry['http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label'] = [item for item in entry['http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label'] if (item != 'person') and (item != 'Person') and (item != 'agent') and (item != 'owl#Thing') and (not item.startswith('DUL.owl#')) and (not item.startswith('Q'))]
        a_people_uni.append(entry)



# Write column headers
with open('a_uni_people.csv', 'w') as csvfile:
    csvfile.write('Title, Birthyear, Nationality, Occuption, Field, Alma mater,  University,  College,  Education, Known for, filtered typelabel\n')
    fieldnames = ['title', 'ontology/birthYear', 'ontology/nationality_label', 'ontology/occupation_label', 'ontology/field_label', 'ontology/almaMater_label', 'ontology/university_label', 'ontology/college_label', 'ontology/education_label', 'ontology/knownFor_label', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    for person in a_people_uni:
        writer.writerow(person)

