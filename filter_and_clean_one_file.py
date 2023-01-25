import json
import csv


# Load JSON list of dictionaries
with open('People/A_people.json') as file:
    a_people_all = json.load(file)


excluded_no = 0
a_people = []
a_people_uni = []


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



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 #defining their occupational groups

#thus, we are left with all non-fictional, non-criminal people that went to uni in our list of dictionaries 'a_people'
occupation_keys = ['ontology/occupation_label','ontology/field_label', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type_label']

for entry in a_people:
    searcharea = []
    for key in occupation_keys:
        if key in entry:
            if type(entry[key]) is list:
                searcharea.extend(entry[key])
            else:
                searcharea.append(entry[key])
          

        is_athlete = False
        if 'athlete' in searcharea:
            is_athlete = True
        if is_athlete:
            entry['occupational_group'] = 'athlete'


        is_academic = False   
        if 'scientist' in searcharea:
            is_academic = True
        if is_academic:
            entry['occupational_group'] = 'academic'


        is_author = False    
        if 'writer' in searcharea:
            is_author = True
        if is_author:
            entry['occupational_group'] = 'author'
            

        is_official = False    
        if 'office holder' in searcharea:
            is_official = True
        if is_official:
            entry['occupational_group'] = 'office_holder'

        is_artist = False
        if 'artist' in searcharea:
            is_artist = True
        if is_artist:
            entry['occupational_group'] = 'artist'

        is_legal = False
        if 'lawyer' in searcharea:
            is_legal = True
        if is_legal:
            entry['occupational_group'] = 'judiciary'
        
        is_actor = False
        if 'actor' in searcharea:
            is_actor = True
        if is_actor:
            entry['occupational_group'] = 'actor'

        is_politician = False
        if 'politician' in searcharea:
            is_politician = True
        if is_politician:
            entry['occupational_group'] = 'politician'
        
        is_religious = False
        if 'bishop' in searcharea:
            is_religious = True
        if is_religious:
            entry['occupational_group'] = 'religious_figure'

        is_royal = False
        if 'monarch' in searcharea:
            is_royal = True
        if is_royal:
            entry['occupational_group'] = 'royalty'

        else:
            entry['occupational_group'] = searcharea

# Write column headers and export our data into a usable csv
with open('a_uni_people.csv', 'w') as csvfile:
    csvfile.write('Title, Birthyear, occupationgroup\n')
    fieldnames = ['title', 'ontology/birthYear', 'occupational_group']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    for person in a_people:
        writer.writerow(person) 



