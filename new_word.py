import pandas as pd

# Load the Excel file
file_path = 'output_file_with_frequency.xlsx'
df = pd.read_excel(file_path)

# Initialize a set to track all characters seen so far
seen_characters = set()

# Function to identify new words in a sentence
def get_new_words(sentence, seen_characters):
    # Extract characters from the sentence
    sentence_chars = set(sentence.replace(" ", ""))  # Remove spaces and convert to a set of unique characters
    # New words are the characters that haven't been seen before
    new_words = sentence_chars - seen_characters
    # Update the seen characters with the new ones
    seen_characters.update(sentence_chars)
    return ''.join(sorted(new_words))  # Return new words as a sorted string

# Apply the function to the DataFrame
df['new word'] = df['sentences'].apply(lambda x: get_new_words(x, seen_characters))

# Save the modified DataFrame to a new Excel file
output_file = 'output_file_with_new_words.xlsx'
df.to_excel(output_file, index=False)

print(f"New words have been added. The updated file is saved as {output_file}.")
