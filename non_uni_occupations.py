import json
import csv

people_in_total = []
excluded_no = 0
people_output = []

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

#defining the labels for each occupation
label_mapping = {
    'athlete': ['athlet', 'coach', 'sport', 'ball'], 
    'academic': ['scienti', 'professor', 'economist', 'philosopher', 'science', 'intellectual', 'histor', 'linguist', 'chem', 'philos', 'astronomy', 'scholar', 'math', 'engineer', 'biolog'],
    'author/journalist': ['writer', 'journalist' ,'author', 'novel'],
    'office_holder': ['office holder', 'president', 'chairman', 'executive', 'mayor', 'united nations'], 
    'artist':['artist', 'musician', 'photographer', 'poet', 'design', 'singer', 'voice', 'dance', 'composer', 'animator', 'sculpt','cartoonist', 'paint', 'music'],
    'judiciary': ['lawyer', 'judge', 'court', 'legal', 'law', 'attorney'],
    'actor': ['actor', 'film', 'producer', 'presenter'],
    'politician':['politician', 'political', 'minist', 'parliament', 'mayor', 'polit', 'diplomat'],
    'religious_figure' : ['bishop', 'pope', 'christian', 'rabbi', 'church', 'faith', 'buddhis'],
    'royalty': ['monarch', 'queen', 'king', 'prince'],
    'medical_field': ['physician', 'surgeon', 'nurse','med', 'neuro', 'surg', 'optometry', 'physical therapy', 'health'],
    'business_person': ['business', 'entrepreneur', 'corpor', 'investor'],
    'military':['military', 'officer', 'marines']
}



#----------------------------------------------------------------------------------------------------------------------------------------------
#filtering data - includes only real non-criminals that list a university

for i in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:

    # Load JSON list of dictionaries
    with open(f'People/{i}_people.json') as file:
        people_all = json.load(file)


    people_in = []

    #filtering out all non-persons and criminals
    for entry in people_all:
        is_fictional = any('fictional' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
        is_criminal = any('criminal' in label.lower() for label in entry["http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label"])
        
        if is_fictional or is_criminal:
            excluded_no += 1
        else:
            people_in.append(entry)


    people_in_total += people_in


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 #defining their occupational groups

#defining the labels in our original dictionary that might contain occupational info and storing this as individual list items to be checked
occupation_keys = ['ontology/occupation_label','ontology/field_label', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label']

for entry in people_in_total:
    searcharea = []
    for key in occupation_keys:
        if key in entry:
            if type(entry[key]) is list:
                searcharea.extend(entry[key])
            elif entry[key] != '':
                searcharea.append(entry[key])
    
    searcharea = [searchareum.lower() for searchareum in searcharea if len(searchareum) >0 and not searchareum[-1].isdigit()] #lowercasing our potential occupations #and removing info of the form ___digit that are not informational in our data

    #fixing some problems in the data where sometimes the birthyear is a list with the first entry not being a likely year but the second is
    if 'ontology/birthYear' in entry:
        if type(entry['ontology/birthYear']) is list:
            entry['ontology/birthYear'] = entry['ontology/birthYear'][1]

    
    #doing our actual checks
    has_occupation = False
    for occupation, labels in label_mapping.items():
        if check_labels(searcharea, labels):
            people_output.append(extract_entry(entry, occupation))
            has_occupation = True

    if not has_occupation and len(searcharea) != 0:
        people_output.append(extract_entry(entry, 'other'))
    

names_list = [output['Title'] for output in people_output]
unique_names = set(names_list) 
#----------------------------------------------------------------------------------------------------------------------------------------------------
#exporting into csv and checking the amounts of observations

print('number excluded:', excluded_no)
print('number included', len(people_in_total))
print(len(names_list))
print(len(unique_names))
 
# Write column headers and export our data into a usable csv
with open('people_output_non_uni.csv', 'w') as csvfile:
    fieldnames = ['Title', 'Birthyear', 'Occupational_group']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    writer.writeheader()
    for person in people_output:
        writer.writerow(person) 

