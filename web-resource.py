import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse
import time
import logging
from pathlib import Path

class WebsiteScraper:
    def __init__(self, base_url, output_dir="scraped_website"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create output directory
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
    def get_page_content(self, url):
        """Fetch the content of a webpage"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def download_file(self, url, local_path):
        """Download a file from URL to local path"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"Downloaded: {url} -> {local_path}")
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading {url}: {e}")
            return False
    
    def extract_css_links(self, soup):
        """Extract CSS file links from HTML"""
        css_links = []
        
        # External CSS files
        for link in soup.find_all('link', {'rel': 'stylesheet'}):
            href = link.get('href')
            if href:
                css_links.append(urljoin(self.base_url, href))
        
        # Inline CSS
        for style in soup.find_all('style'):
            if style.string:
                css_links.append(('inline', style.string))
        
        return css_links
    
    def extract_js_links(self, soup):
        """Extract JavaScript file links from HTML"""
        js_links = []
        
        # External JS files
        for script in soup.find_all('script', {'src': True}):
            src = script.get('src')
            if src:
                js_links.append(urljoin(self.base_url, src))
        
        # Inline JavaScript
        for script in soup.find_all('script'):
            if script.string and not script.get('src'):
                js_links.append(('inline', script.string))
        
        return js_links
    
    def extract_image_links(self, soup):
        """Extract image links from HTML"""
        image_links = []
        
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                image_links.append(urljoin(self.base_url, src))
        
        return image_links
    
    def sanitize_filename(self, url):
        """Create a safe filename from URL"""
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1]
        
        if not filename or filename == '/':
            filename = 'index.html'
        
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return filename
    
    def update_html_links(self, html_content, css_files, js_files, image_files):
        """Update HTML to point to local files"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Update CSS links
        for link in soup.find_all('link', {'rel': 'stylesheet'}):
            href = link.get('href')
            if href:
                full_url = urljoin(self.base_url, href)
                if full_url in css_files:
                    local_path = css_files[full_url]
                    link['href'] = local_path
        
        # Update JavaScript links
        for script in soup.find_all('script', {'src': True}):
            src = script.get('src')
            if src:
                full_url = urljoin(self.base_url, src)
                if full_url in js_files:
                    local_path = js_files[full_url]
                    script['src'] = local_path
        
        # Update image links
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                full_url = urljoin(self.base_url, src)
                if full_url in image_files:
                    local_path = image_files[full_url]
                    img['src'] = local_path
        
        return str(soup)
    
    def scrape_website(self):
        """Main scraping function"""
        self.logger.info(f"Starting to scrape: {self.base_url}")
        
        # Get main HTML content
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            self.logger.error("Failed to fetch main page")
            return
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract all resource links
        css_links = self.extract_css_links(soup)
        js_links = self.extract_js_links(soup)
        image_links = self.extract_image_links(soup)
        
        # Track downloaded files
        downloaded_css = {}
        downloaded_js = {}
        downloaded_images = {}
        
        # Download CSS files
        css_dir = os.path.join(self.output_dir, 'css')
        os.makedirs(css_dir, exist_ok=True)
        
        for i, css_link in enumerate(css_links):
            if isinstance(css_link, tuple) and css_link[0] == 'inline':
                # Save inline CSS
                filename = f"inline_style_{i}.css"
                local_path = os.path.join(css_dir, filename)
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(css_link[1])
                self.logger.info(f"Saved inline CSS: {local_path}")
            else:
                # Download external CSS
                filename = self.sanitize_filename(css_link)
                if not filename.endswith('.css'):
                    filename += '.css'
                
                local_path = os.path.join(css_dir, filename)
                if self.download_file(css_link, local_path):
                    downloaded_css[css_link] = f"css/{filename}"
                
                time.sleep(0.1)  # Be respectful to the server
        
        # Download JavaScript files
        js_dir = os.path.join(self.output_dir, 'js')
        os.makedirs(js_dir, exist_ok=True)
        
        for i, js_link in enumerate(js_links):
            if isinstance(js_link, tuple) and js_link[0] == 'inline':
                # Save inline JavaScript
                filename = f"inline_script_{i}.js"
                local_path = os.path.join(js_dir, filename)
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(js_link[1])
                self.logger.info(f"Saved inline JavaScript: {local_path}")
            else:
                # Download external JavaScript
                filename = self.sanitize_filename(js_link)
                if not filename.endswith('.js'):
                    filename += '.js'
                
                local_path = os.path.join(js_dir, filename)
                if self.download_file(js_link, local_path):
                    downloaded_js[js_link] = f"js/{filename}"
                
                time.sleep(0.1)  # Be respectful to the server
        
        # Download images
        img_dir = os.path.join(self.output_dir, 'images')
        os.makedirs(img_dir, exist_ok=True)
        
        for img_link in image_links:
            filename = self.sanitize_filename(img_link)
            local_path = os.path.join(img_dir, filename)
            if self.download_file(img_link, local_path):
                downloaded_images[img_link] = f"images/{filename}"
            
            time.sleep(0.1)  # Be respectful to the server
        
        # Update HTML to use local files
        updated_html = self.update_html_links(html_content, downloaded_css, downloaded_js, downloaded_images)
        
        # Save updated HTML
        html_path = os.path.join(self.output_dir, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        self.logger.info(f"Scraping completed! Files saved to: {self.output_dir}")
        
        # Print summary
        print(f"\nScraping Summary:")
        print(f"Website: {self.base_url}")
        print(f"Output directory: {self.output_dir}")
        print(f"CSS files downloaded: {len(downloaded_css)}")
        print(f"JavaScript files downloaded: {len(downloaded_js)}")
        print(f"Images downloaded: {len(downloaded_images)}")
        print(f"Main HTML saved as: index.html")

def main():
    """Main function to run the scraper"""
    print("Website Scraper")
    print("=" * 50)
    
    # Get URL from user
    url = input("Enter the website URL to scrape: ").strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Get output directory (optional)
    output_dir = input("Enter output directory (press Enter for default 'scraped_website'): ").strip()
    if not output_dir:
        output_dir = "scraped_website"
    
    # Create scraper instance and run
    scraper = WebsiteScraper(url, output_dir)
    
    try:
        scraper.scrape_website()
        print(f"\nScraping completed successfully!")
        print(f"Open '{output_dir}/index.html' in your browser to view the scraped website.")
    except Exception as e:
        print(f"Error occurred during scraping: {e}")

if __name__ == "__main__":
    main()