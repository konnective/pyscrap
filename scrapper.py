import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import json

class WebDevScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results = []
    
    def search_duckduckgo(self, city, num_results=20):
        """Search DuckDuckGo for web development companies"""
        query = f"web development company {city}"
        print(f"Searching DuckDuckGo for: {query}")
        
        try:
            # DuckDuckGo HTML search
            url = "https://html.duckduckgo.com/html/"
            data = {'q': query}
            
            response = requests.post(url, data=data, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all result links
            results = soup.find_all('a', class_='result__a')
            
            urls = []
            for result in results[:num_results]:
                if 'href' in result.attrs:
                    url = result['href']
                    if url.startswith('http'):
                        urls.append(url)
            
            print(f"Found {len(urls)} URLs from DuckDuckGo")
            return urls
        
        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")
            return []
    
    def search_bing(self, city, num_results=20):
        """Search Bing for web development companies"""
        query = f"web development company {city}"
        print(f"Searching Bing for: {query}")
        
        try:
            url = f"https://www.bing.com/search?q={query}&count={num_results}"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all organic search results
            results = soup.find_all('li', class_='b_algo')
            
            urls = []
            for result in results:
                link = result.find('a')
                if link and 'href' in link.attrs:
                    url = link['href']
                    if url.startswith('http') and 'bing.com' not in url:
                        urls.append(url)
            
            print(f"Found {len(urls)} URLs from Bing")
            return urls
        
        except Exception as e:
            print(f"Error searching Bing: {e}")
            return []
    
    def manual_search(self, city):
        """Provide manual search options"""
        print(f"\nAlternative: Use these directories to find web dev companies in {city}:")
        print(f"1. https://clutch.co/web-developers/{city.lower().replace(' ', '-')}")
        print(f"2. https://www.goodfirms.co/directory/country/web-development")
        print(f"3. https://www.designrush.com/agency/web-development")
        print(f"4. Google Maps: Search 'web development company {city}'")
        print(f"\nYou can also manually input URLs below.")
        
        urls = []
        print("\nEnter URLs manually (press Enter without input to finish):")
        while True:
            url = input("URL: ").strip()
            if not url:
                break
            if url.startswith('http'):
                urls.append(url)
        
        return urls
    
    def extract_company_info(self, url):
        """Extract basic information from a company website"""
        try:
            print(f"  Extracting info from: {url}")
            response = requests.get(url, headers=self.headers, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else "N/A"
            if title:
                title = title.strip()
            
            # Extract meta description
            description = "N/A"
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and 'content' in meta_desc.attrs:
                description = meta_desc['content'][:200]
            
            # Try to extract email (be more flexible)
            email = "N/A"
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            
            # Check contact page
            text_content = soup.get_text()
            emails = re.findall(email_pattern, text_content)
            # Filter out common non-business emails
            business_emails = [e for e in emails if not any(x in e.lower() for x in ['example.com', 'test.com', 'sentry.io'])]
            if business_emails:
                email = business_emails[0]
            
            # Try to extract phone
            phone = "N/A"
            phone_patterns = [
                r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            ]
            
            for pattern in phone_patterns:
                phones = re.findall(pattern, text_content)
                if phones:
                    phone = phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
                    break
            
            return {
                'url': url,
                'title': title,
                'description': description,
                'email': email,
                'phone': phone
            }
        
        except Exception as e:
            print(f"  Error: {e}")
            return {
                'url': url,
                'title': 'Error loading',
                'description': 'N/A',
                'email': 'N/A',
                'phone': 'N/A'
            }
    
    def scrape_city(self, city, method='bing', num_results=20):
        """Main method to scrape web dev companies in a city"""
        print(f"\n{'='*60}")
        print(f"Scraping Web Development Companies in {city}")
        print(f"{'='*60}\n")
        
        urls = []
        
        if method == 'bing':
            urls = self.search_bing(city, num_results)
        elif method == 'duckduckgo':
            urls = self.search_duckduckgo(city, num_results)
        elif method == 'manual':
            urls = self.manual_search(city)
        else:
            # Try multiple methods
            urls.extend(self.search_bing(city, num_results))
            if len(urls) < 5:
                urls.extend(self.search_duckduckgo(city, num_results))
        
        # Remove duplicates
        urls = list(set(urls))
        
        if not urls:
            print("\nNo results found! Try the manual method or use web directories.")
            self.manual_search(city)
            return
        
        print(f"\nFound {len(urls)} unique URLs. Extracting information...\n")
        
        # Extract info from each URL
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}]")
            
            info = self.extract_company_info(url)
            if info:
                self.results.append(info)
            
            # Be respectful - add delay between requests
            time.sleep(3)
        
        print(f"\n{'='*60}")
        print(f"Successfully scraped {len(self.results)} companies")
        print(f"{'='*60}\n")
    
    def save_to_csv(self, filename):
        """Save results to CSV file"""
        if not self.results:
            print("No results to save!")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'title', 'description', 'email', 'phone'])
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"✓ Results saved to {filename}")
    
    def display_results(self):
        """Display results in console"""
        if not self.results:
            print("No results to display!")
            return
        
        for i, result in enumerate(self.results, 1):
            print(f"\n{'─'*60}")
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Description: {result['description'][:100]}...")
            print(f"   Email: {result['email']}")
            print(f"   Phone: {result['phone']}")


# Example usage
if __name__ == "__main__":
    print("Web Development Company Scraper")
    print("="*60)
    
    scraper = WebDevScraper()
    
    # Enter the city you want to search
    city = input("\nEnter city name: ")
    
    print("\nSearch methods:")
    print("1. Bing (recommended)")
    print("2. DuckDuckGo")
    print("3. Manual input")
    print("4. Try all methods")
    
    method_choice = input("Choose method (1-4): ").strip()
    
    method_map = {
        '1': 'bing',
        '2': 'duckduckgo',
        '3': 'manual',
        '4': 'all'
    }
    
    method = method_map.get(method_choice, 'bing')
    
    num_results = 20
    if method != 'manual':
        num_results = int(input("Number of results to fetch (default 20): ") or "20")
    
    # Scrape the city
    scraper.scrape_city(city, method, num_results)
    
    # Display results
    if scraper.results:
        scraper.display_results()
        
        # Save to CSV
        save = input("\nSave to CSV? (y/n): ")
        if save.lower() == 'y':
            filename = f"web_dev_companies_{city.replace(' ', '_')}.csv"
            scraper.save_to_csv(filename)
    else:
        print("\n⚠ No results were scraped. Consider:")
        print("  - Using the manual input method")
        print("  - Checking web directories like Clutch.co")
        print("  - Using official APIs (Google Places, Yelp)")