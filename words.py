import requests
from bs4 import BeautifulSoup
import re

# Function to extract words from a webpage
def extract_words_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text)
        return words
    else:
        print("Failed to retrieve the page.")
        return []

# Take URL input from the user
url = input("Enter the URL of the webpage: ")
words = extract_words_from_page(url)

# Display the extracted words
print("\nExtracted words from the page:")
print(words)