import json

with open('dataset.json', 'r') as f:
    data = json.load(f)

new_intent = {
    "tag": "first_year_subjects",
    "patterns": [
        "how many subjects in first year",
        "first year subjects",
        "what are the subjects in first year",
        "1st year subjects",
        "subjects for first year"
    ],
    "response": "First year Engineering typically has 6 subjects per semester, including Engineering Mathematics, Physics/Chemistry, Basic Electrical Engineering, Programming in C/Python, and Engineering Graphics. You also have 3-4 practical labs."
}

# Add "how many subjects" to syllabus as well just in case
for item in data:
    if item.get('intent') == 'syllabus_download' or item.get('tag') == 'syllabus':
        item['patterns'].extend(["how many subjects", "number of subjects", "list of subjects"])

data.append(new_intent)

with open('dataset.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))
print("Dataset updated successfully.")
