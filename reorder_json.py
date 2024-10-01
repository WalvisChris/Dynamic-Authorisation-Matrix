# To test a function before implementing it into the main dam demo.py
import json

switch = [0, 0]

file_name = 'example' # set to example for github push
file_path = f'data_{file_name}.JSON'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

switch[0] = int(input("Enter index A (int): "))
switch[1] = int(input("Enter index B (int): "))

data['Columns'][switch[0]], data['Columns'][switch[1]] = data['Columns'][switch[1]], data['Columns'][switch[0]]

with open(file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)