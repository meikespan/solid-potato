import json

# Load JSON list of dictionaries
with open('A_people.json') as file:
    a_people = json.load(file)


a_people_uni = []

#filtering for all people that went to university
for entry in a_people:
    if 'University' in entry: #filter out for all entries in list that contain the word  "university"
        a_people_uni.append(entry)

print(a_people_uni)