import pandas as pd

# Load the Excel file
df = pd.read_excel('../xlsx/words_with_examples.xlsx')

# Convert DataFrame to JSON
json_data = df.to_json(orient='records', force_ascii=False)

# Save to a file
with open('../words_with_examples.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print('Conversion complete! JSON file saved as words_with_examples.json')
