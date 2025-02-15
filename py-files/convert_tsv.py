import pandas as pd

# Load the .tsv file into a pandas DataFrame
input_file = 'cmn_sen_db_2.tsv'  # Path to your .tsv file
output_file = 'output_file.xlsx'  # Path to the output Excel file

# Read the file, assuming tab-separated values
df = pd.read_csv(input_file, sep='\t', header=None)

# Select the columns you need (number, simplified, pinyin, translation)
df_filtered = df[[0, 1, 3, 4]]

# Rename the columns to match your desired output
df_filtered.columns = ['Number', 'Simplified', 'Pinyin', 'Translation']

# Save the filtered data to an Excel file
df_filtered.to_excel(output_file, index=False)

print(f"File has been successfully converted to {output_file}")
