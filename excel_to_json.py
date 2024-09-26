import pandas as pd

# Load xlsx
file_path = r'C:\Users\chris\Downloads\Stage Doove\Ontvangen Data\B-410a Informatieclassificatie & autorisatiematrix.xlsx'
df = pd.read_excel(file_path, sheet_name='Classificatie')
df.columns = df.columns.str.strip()

# Modify str
def column_to_json(column_data):
    title = str(column_data.iloc[4])
    values = column_data.iloc[5:]
    
    str1 = '\t"Title": "' + title + '",'
    tmp = ''.join(values.astype(str))
    tmp = tmp.replace('nan', '').replace('  ', ' ')
    str2 = '\t"Values": ['
    for letter in tmp:
        str2 = str2 + '"' + letter.upper() + '", '
    str2 = str2[:-2] + "]"
    result = str1 + "\n" + str2
    print(result)

# Output
print("Column Names: ", df.columns)
for col_index in range(8, 70):
    print('},')
    print('{')
    column_data = df.iloc[:, col_index]
    column_to_json(column_data)
print('}')
