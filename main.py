# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(url):
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage: {e}")
        return []
    
    # Parse the content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the anchor tags (<a>) and convert relative URLs to absolute URLs
    links = [urljoin(url, a.get('href')) for a in soup.find_all('a') if a.get('href') is not None]
    
    return links

# URL of the website you want to scrape
startingUrl = 'https://example.com'
depth = 2

allLinks = [[startingUrl]]

for i in range(depth):
    newLinks = []
    for link in allLinks[i]:
        newLinks.extend(get_all_links(link))
    allLinks.append(newLinks)

print(allLinks)
