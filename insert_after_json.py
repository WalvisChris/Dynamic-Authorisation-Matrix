# To test a function before implementing it into the main dam demo.py
import json

file_name = 'example' # set to example for github push
file_path = f'data_{file_name}.JSON'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

column_index = int(input("Enter index to insert (int): "))
insert_index = int(input("Enter index to insert after (int): "))

columns = data['Columns']
    
insert_position = insert_index + 1

if 0 <= column_index < len(columns):
    column_to_insert = columns[column_index]
    
    del columns[column_index]
    
    columns.insert(insert_position, column_to_insert)

with open('output.txt', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)