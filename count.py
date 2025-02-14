import json
from collections import defaultdict

import pandas as pd
from tqdm import tqdm

# Load the Excel file
df = pd.read_excel('output_file_with_new_words.xlsx')

# Load the JSON file
with open('complete.min.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Create a dictionary with HSK levels as keys
hsk_word_map = defaultdict(set)

for entry in json_data:
    word = entry.get('s')
    levels = entry.get('l', [])
    for level in levels:
        if level.startswith('n'):  # Only consider new HSK levels
            hsk_level = level.replace('n', 'hsk')
            hsk_word_map[hsk_level].add(word)

# Check for overlapping words and track missing words
hsk_overlap = defaultdict(int)
hsk_totals = {level: len(words) for level, words in hsk_word_map.items()}
missing_words = []

for hsk_level, words in tqdm(hsk_word_map.items()):
    for word in words:
        if df['sentences'].str.contains(word).any():
            hsk_overlap[hsk_level] += 1
        else:
            missing_words.append((hsk_level, word))

# Calculate and display the overlap percentage per level
for level, matched in hsk_overlap.items():
    total = hsk_totals[level]
    percentage = (matched / total * 100) if total > 0 else 0
    print(f"HSK Level {level}: {percentage:.2f}% ({matched}/{total})")

# Save missing words to a text file
# with open('not_matched_words.txt', 'w', encoding='utf-8') as f:
#     f.write("HSK Level\tWord\n")
#     for level, word in missing_words:
#         f.write(f"{level}\t{word}\n")

# Optionally, save to an Excel file
missing_df = pd.DataFrame(missing_words, columns=['HSK Level', 'Word'])
missing_df.to_excel('not_matched_words.xlsx', index=False)

# print("Missing words saved to 'not_matched_words.txt' and 'not_matched_words.xlsx'")")
# }
