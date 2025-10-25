import requests
from bs4 import BeautifulSoup

## returns a dict of event titles and hrefs

##TODO:Allow users to update the URL to scrape different pages if needed 

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        titles_raw = soup.find_all('h2')
        titles = [title.get_text(strip=True) for title in titles_raw]
        hrefs = [title.find('a')['href'] for title in titles_raw if title.find('a')] 
        events = dict(zip(titles, hrefs))
        
        print(events)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}") 
        return

if __name__ == "__main__":
    url = "https://secretglasgow.com/things-to-do-october-glasgow/"
    scrape_website(url)