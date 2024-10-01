import json

file_name = 'example' # set to example for github push
file_path = f'data_{file_name}.JSON'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

print("Loaded data:", data)

if 'Columns' in data:
    for column in data['Columns']:
        if 'Values' in column and isinstance(column['Values'], list):
            column['Values'] = "".join(column['Values'])
            print(f"Updated Values for '{column['Title']}':", column['Values'])

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)

print("Data written to file.")