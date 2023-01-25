import json
import csv


# Load JSON list of dictionaries
with open('People/A_people.json') as file:
    a_people_all = json.load(file)


excluded_no = 0
a_people = []
a_people_uni = []
a_people_output = []


#filtering for uni education
for entry in a_people_all:
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

#filtering out all non-persons and criminals
for entry in a_people_uni:
    is_fictional = any('fictional' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
    is_criminal = any( 'criminal' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
     
    if is_fictional or is_criminal:
        excluded_no += 1
    else:
        a_people.append(entry)


#fixing some problems in the data where sometimes the birthyear is a list with the first entry not being a likely year but the second is
for entry in a_people:
    if 'ontology/birthYear' in entry:
        if type(entry['ontology/birthYear']) is list:
            entry['ontology/birthYear'] = entry['ontology/birthYear'][1]



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 #defining their occupational groups

#thus, we are left with all non-fictional, non-criminal people that went to uni in our list of dictionaries 'a_people'

#defining functions
def extract_entry(entry, label):
    return {
        'Title': entry['title'],
        'Birthyear': entry.get('ontology/birthYear'),
        'Occupational_group': label
    }

def check_labels(look_heres, labels):
    for label in labels:
        for look_here in look_heres:
            if label in look_here:
                return True
            else:
                return False

athlete_labels = ['athlete', 'coach', 'sport']
academic_labels = ['scientist', 'professor', 'historian','economist']
writer_labels = ['writer', 'journalist' ,'author']
official_labels = ['office holder']
artist_labels = ['artist', 'musician', 'photographer', 'poet']
legal_labels = ['lawyer', 'judge']
actor_labels = ['actor']
politician_labels = ['politician']
religious_labels = ['bishop', 'pope']
royal_labels = ['monarch', 'queen', 'king']
medical_labels = ['physician', 'surgeon', 'nurse','med']
business_labels = ['business', 'entrepreneur']

#defining the labels in our original dictionary that might contain occupational info and storing this as individual list items to be checked
occupation_keys = ['ontology/occupation_label','ontology/field_label', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label']


for entry in a_people:
    searcharea = []
    for key in occupation_keys:
        if key in entry:
            if type(entry[key]) is list:
                searcharea.extend(entry[key])
            elif entry[key] != '':
                searcharea.append(entry[key])
    
    searcharea = [searchareum.lower() for searchareum in searcharea if not searchareum[-1].isdigit()] #lowercasing our potential occupations and removing info of the form ___digit that are not informational in our data
    
    # #setting our default value for the new column 'occupational_group'
    # entry['occupational_group'] = 'other'


    if check_labels(searcharea, athlete_labels):
        a_people_output.append(extract_entry(entry, 'athlete'))
    
    elif check_labels(searcharea, academic_labels):
        a_people_output.append(extract_entry(entry, 'academic'))
    
    elif check_labels(searcharea, writer_labels):
        a_people_output.append(extract_entry(entry, 'author/journalist'))

    elif check_labels(searcharea, official_labels):
        a_people_output.append(extract_entry(entry, 'office_holder'))
    
    elif check_labels(searcharea, artist_labels):
        a_people_output.append(extract_entry(entry, 'artist'))

    elif check_labels(searcharea, legal_labels):
        a_people_output.append(extract_entry(entry, 'judiciary'))

    elif check_labels(searcharea, actor_labels):
        a_people_output.append(extract_entry(entry, 'actor'))

    elif check_labels(searcharea, politician_labels):
        a_people_output.append(extract_entry(entry, 'politician'))

    elif check_labels(searcharea, religious_labels):
        a_people_output.append(extract_entry(entry, 'religious_figure'))
    
    elif check_labels(searcharea, royal_labels):  
        a_people_output.append(extract_entry(entry, 'royalty'))

    elif check_labels(searcharea, medical_labels):  
        a_people_output.append(extract_entry(entry, 'medical_field'))

    elif check_labels(searcharea, business_labels):
        a_people_output.append(extract_entry(entry, 'business_person'))

    else:
        a_people_output.append(extract_entry(entry, 'other'))
    
 
 
# Write column headers and export our data into a usable csv
with open('a_people_output_try.csv', 'w') as csvfile:
    fieldnames = ['Title', 'Birthyear', 'Occupational_group']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    writer.writeheader()
    for person in a_people_output:
        writer.writerow(person) 





