import requests
from bs4 import BeautifulSoup

## returns a dict of event titles and hrefs

##TODO:Allow users to update the URL to scrape different pages if needed 

def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def find_titles_and_hrefs(url, title_tag):
        soup = fetch_page(url)
        titles_raw = soup.find_all(title_tag)
        titles = [title.get_text(strip=True) for title in titles_raw]
        hrefs = [title.find('a')['href'] for title in titles_raw if title.find('a')] 
        events = dict(zip(titles, hrefs))
        return events

def find_reviews(url, title_tag=None):
    soup = fetch_page(url)
    all_links = soup.find_all("a")

    data = []
    current_title = None
    current_cats = []

    for link in all_links:
        classes = link.get("class", [])
        
        # Title link
        if "link-white-to-secondary-20" in classes:
            # Save previous title + categories
            if current_title:
                data.append([current_title, current_cats])
            current_title = link.get_text(strip=True)
            current_cats = []
        
        # Category link
        elif "font-size-90" in classes:
            current_cats.append(link.get_text(strip=True))
    
    # Add last title
    if current_title:
        data.append([current_title, current_cats])
    
    return data


def event_scrape_website(url):
    try:
        events = find_titles_and_hrefs(url, 'h2')
        return events
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}") 
        return

def pub_scrape_website(url):
    try:
        pubs = find_reviews(url, 'div')
        return pubs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}") 
        return

if __name__ == "__main__":
    #temporary variable to decide what type of scraping to do
    event = False
    pub = True
    event_url = "https://secretglasgow.com/things-to-do-october-glasgow/"
    pub_url = "https://www.designmynight.com/glasgow/bars/cool-and-quirky-bars-in-glasgow"

    if event == True:
        events = event_scrape_website(event_url)
    if pub == True:
        events = pub_scrape_website(pub_url)
        print(events[1])