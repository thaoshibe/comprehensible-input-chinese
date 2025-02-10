import csv
import time
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from tqdm import tqdm  # Import tqdm for the progress bar

# Set up Selenium to run in headless mode
options = Options()
options.headless = True

# Function to initialize multiple drivers
def init_drivers(num_drivers=10):
    drivers = []
    for _ in range(num_drivers):
        drivers.append(webdriver.Chrome(options=options))
    return drivers

# Function to fetch top 3 examples for a word using a specific driver
def fetch_examples(driver, word):
    try:
        # Go to the URL with the word query
        url = f"https://english.dict.naver.com/english-chinese-dictionary/#/search?range=example&query={word}"
        driver.get(url)

        # Wait for the page to load completely
        time.sleep(1)

        # Extract the examples from <p> tags with class 'text' and language 'zh_CN'
        examples = driver.find_elements(By.CSS_SELECTOR, 'p.text[lang="zh_CN"]')

        # Get the top 3 examples (or fewer if there aren't enough)
        return "\n".join([example.text for example in examples[:3]])
    except Exception as e:
        print(f"Error fetching examples for {word}: {e}")
        return ""  # Return empty string if an error occurs

# Read from the CSV file and process the words
with open('output.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    
    # Create a list of rows to be processed
    rows = list(reader)[:1000]  # Limit to the first 100 rows

    # Create a list of rows to be written back to CSV
    updated_rows = []

    # Initialize the WebDriver instances (10 drivers)
    drivers = init_drivers(num_drivers=10)

    # Create a ThreadPoolExecutor to fetch examples in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        for row in tqdm(rows):
            # Get the word(s) from the high-freq column
            high_freq_words = row['high-freq'].split('\n')  # Assuming words are separated by newline

            # Distribute the fetching tasks among the drivers
            future_to_word = {}
            driver_idx = 0
            for word in high_freq_words:
                future = executor.submit(fetch_examples, drivers[driver_idx], word.strip())
                future_to_word[future] = word.strip()
                driver_idx = (driver_idx + 1) % len(drivers)  # Rotate through the drivers

            # Collect all the results from the futures
            examples = []
            for future in future_to_word:
                try:
                    example = future.result()  # Get result (this will block until the result is available)
                    examples.append(example)
                except Exception as e:
                    print(f"Error retrieving examples for {future_to_word[future]}: {e}")
                    examples.append("")  # If there's an error, append an empty string

            # Join the examples for all words
            row['examples'] = "\n".join(examples)
            print(examples)
            updated_rows.append(row)

    # Write the updated rows back to the CSV
    with open('output_with_examples.csv', mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = reader.fieldnames + ['examples']  # Add 'examples' column
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write the header and updated rows
        writer.writeheader()
        writer.writerows(updated_rows)

    # Close all the drivers after execution
    for driver in drivers:
        driver.quit()

print("Finished processing all words.")
