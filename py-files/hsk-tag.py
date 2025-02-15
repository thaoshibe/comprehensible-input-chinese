import json
import re

import pandas as pd

# Load the Excel file into a DataFrame
excel_file = 'output_file_with_new_words.xlsx'
df = pd.read_excel(excel_file)

# Load the JSON file
json_file = 'complete.min.json'
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Create a dictionary from the JSON data for fast lookup
word_info = {}
for entry in json_data:
    simplified = entry.get("s")
    level = entry.get("l", [])
    hsk_tag = next((tag.replace('n', 'hsk') for tag in level if tag.startswith('n')), None)

    # Aggregate all pinyin and meanings
    pinyin_list = []
    meanings_list = []
    for idx, form in enumerate(entry.get("f", [])):
        pinyin = form.get("i", {}).get("y", "")
        meanings = ', '.join(form.get("m", []))
        if pinyin and meanings:
            pinyin_list.append(f"* {pinyin}")
            meanings_list.append(f"* {meanings}")

    word_info[simplified] = {
        'hsk-tag': hsk_tag,
        'pinyin': '\n'.join(pinyin_list),
        'meanings': '\n'.join(meanings_list)
    }

# Function to check if a word contains only Chinese characters
def is_chinese(word):
    return bool(re.match(r'^[\u4e00-\u9fa5]+$', word))

# Create new columns in the DataFrame for hsk-tag, pinyin, and meanings
def get_word_info(words):
    hsk_tag_list = []
    pinyin_list = []
    meanings_list = []

    for char in words:
        if is_chinese(char):
            word_data = word_info.get(char, {})
            hsk_tag = word_data.get('hsk-tag')
            if hsk_tag:
                hsk_tag_list.append(hsk_tag)
            pinyin = word_data.get('pinyin', '')
            if pinyin:
                pinyin_list.append(pinyin)
            meanings = word_data.get('meanings', '')
            if meanings:
                meanings_list.append(f'{char}\n{meanings}')

    return pd.Series({
        'hsk-tag': '\n'.join(filter(None, hsk_tag_list)),
        'pinyin': '\n'.join(filter(None, pinyin_list)),
        'meanings': '\n'.join(filter(None, meanings_list))
    })

# Apply the function to the 'new word' column, splitting into characters if necessary
df[['hsk-tag', 'pinyin-word', 'meanings']] = df['new word'].apply(lambda x: get_word_info(list(str(x))))

# Save the modified DataFrame back to Excel
output_file = 'output_file_with_new_words_updated.xlsx'
df.to_excel(output_file, index=False)

print(f"Updated file saved as {output_file}")
