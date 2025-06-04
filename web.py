import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

def extract_layout(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    layout_tags = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
    layout = []

    for tag in layout_tags:
        elements = soup.find_all(tag)
        for el in elements:
            layout.append(f"<{tag}> - {el.get('id') or el.get('class') or 'no identifier'}")
    
    return layout

def main():
    url = input("Enter a URL: ")
    html = fetch_html(url)

    if html:
        layout = extract_layout(html)
        print("\nSimplified Layout:")
        for tag in layout:
            print(tag)
    else:
        print("Failed to retrieve or parse the page.")

if __name__ == "__main__":
    main()
