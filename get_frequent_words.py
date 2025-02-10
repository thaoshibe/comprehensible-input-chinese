import csv

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# Function to scrape high and medium frequency words for a character
def get_frequency_words(character):
    url = f'https://hanzicraft.com/character/{character}'
    response = requests.get(url)
    
    # Prepare dictionary to store result
    result = {
        "character": character,
        "high-freq": "",
        "medium-freq": "",
    }

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the container for the example words
        examples_section = soup.find('div', class_='examples')

        if examples_section:
            # Find all example word blocks
            word_blocks = examples_section.find_all('div', class_='wordblock')

            high_freq_words = []
            medium_freq_words = []

            for word_block in word_blocks:
                # Get the example word category (High Frequency, Medium Frequency, etc.)
                example_category = word_block.find_previous('h4').text.strip()

                # Get the word and its link
                word_link = word_block.find('a')
                word = word_link.text if word_link else "No word found"

                # Depending on the category, add the word to the correct list
                if "High Frequency" in example_category:
                    high_freq_words.append(word)
                elif "Medium Frequency" in example_category:
                    medium_freq_words.append(word)

            # Convert the list of words to a real newline-separated string (actual line breaks)
            result["high-freq"] = "\n".join(high_freq_words)
            result["medium-freq"] = "\n".join(medium_freq_words)

        else:
            print(f"Examples section not found for character {character}.")
    else:
        print(f"Failed to retrieve the page for character {character}. Status code: {response.status_code}")
    
    return result

# Read the input CSV file containing Chinese characters
with open('3000.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    characters = [row[0] for row in reader]  # Assuming each row has one character

# Prepare the output file to write the results
with open('output.csv', mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["character", "high-freq", "medium-freq"])  # Write headers

    # For each character in the input CSV, get high and medium frequency words
    for character in tqdm(characters[1:]):
        result = get_frequency_words(character)
        
        # Write the result to the output CSV
        writer.writerow([result["character"], result["high-freq"], result["medium-freq"]])

        print(f"Processed {character}")

print("Data has been written to 'output.csv'")
