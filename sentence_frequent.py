import pandas as pd
from tqdm import tqdm

# Step 1: Load the frequency data
frequency_df = pd.read_excel('frequency.xlsx')  # Adjust the path if needed
frequency_dict = pd.Series(frequency_df['rank'].values, index=frequency_df['hanzi'].values).to_dict()

# Step 2: Load the sentence data
output_df = pd.read_excel('output_file.xlsx')  # Adjust the path if needed
# breakpoint()
# Step 3: Define a function to calculate the average frequency rank of a sentence
def calculate_frequency_rank(sentence):
    total_rank = 0
    char_count = 0
    for char in sentence:
        if char in frequency_dict:
            total_rank += frequency_dict[char]
            char_count += 1
    # Avoid division by zero if no valid characters
    if char_count > 0:
        return total_rank / char_count
    else:
        return None  # or 0 if you prefer

# Step 4: Use tqdm to apply the function and show progress bar
tqdm.pandas(desc="Calculating Frequency Rank")

# Apply the function to each sentence and create a new column for frequency rank
output_df['frequency rank'] = output_df['sentences'].progress_apply(calculate_frequency_rank)

# Step 5: Save the updated output to a new file
output_df.to_excel('output_file_with_frequency.xlsx', index=False)

print("The 'frequency rank' has been added to the output file.")
