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

def check_labels(searcharea, labels):
    for label in labels:
        for searchareum in searcharea:
            if label in searchareum:
                return True

athlete_labels = ['athlete', 'coach', 'sport']

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
    
    # is_athlete =False
    # if any('athlete' in searchareum or 'coach' in searchareum or 'sport' in searchareum for searchareum in searcharea):
    #     is_athlete = True
    # if is_athlete:
    #     entry['occupational_group'] = 'athlete'


    # is_academic = False   
    # if any('scientist' in searchareum or 'professor' in searchareum or 'historian' in searchareum or 'economist' in searchareum for searchareum in searcharea):
    #     is_academic = True
    # if is_academic:
    #     entry['occupational_group'] = 'academic'


    # is_writer = False    
    # if any('writer' in searchareum or 'journalist' in searchareum or 'author' in searchareum for searchareum in searcharea):
    #     is_writer = True
    # if is_writer:
    #     entry['occupational_group'] = 'author/journalist'
        

    # is_official = False    
    # if 'office holder' in searcharea:
    #     is_official = True
    # if is_official:
    #     entry['occupational_group'] = 'office_holder'

    # is_artist = False
    # if any('artist' in searchareum or 'musician' in searchareum or 'photographer' in searchareum or 'poet' in searchareum for searchareum in searcharea):
    #     is_artist = True
    # if is_artist:
    #     entry['occupational_group'] = 'artist'

    # is_legal = False
    # if any('lawyer' in searchareum or 'judge' in searchareum for searchareum in searcharea):
    #     is_legal = True
    # if is_legal:
    #     entry['occupational_group'] = 'judiciary'
    
    # is_actor = False
    # if any('actor' in searchareum for searchareum in searcharea):
    #     is_actor = True
    # if is_actor:
    #     entry['occupational_group'] = 'actor'

    # is_politician = False
    # if any('politician' in searchareum for searchareum in searcharea):
    #     is_politician = True
    # if is_politician:
    #     entry['occupational_group'] = 'politician'
    
    # is_religious = False
    # if any('bishop' in searchareum or 'pope' in searchareum for searchareum in searcharea):
    #     is_religious = True
    # if is_religious:
    #     entry['occupational_group'] = 'religious_figure'

    # is_royal = False
    # if 'monarch' in searcharea:
    #     is_royal = True
    # if is_royal:
    #     entry['occupational_group'] = 'royalty'

    # is_medical = False
    # if any('physician' in searchareum or 'surgeon' in searchareum or 'nurse' in searchareum or 'med' in searchareum for searchareum in searcharea):
    #     is_medical = True
    # if is_medical:
    #     entry['occupational_group'] = 'medical'


    # is_business = False
    # if any(('business' in searchareum or 'entrepreneur' in searchareum) for searchareum in searcharea):
    #     is_business = True
    # if is_business:
    #     entry['occupational_group'] = 'business_person'


 
# Write column headers and export our data into a usable csv
with open('a_people_output_try.csv', 'w') as csvfile:
    fieldnames = ['Title', 'Birthyear', 'Occupational_group']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='', extrasaction='ignore')

    writer.writeheader()
    for person in a_people_output:
        writer.writerow(person) 





