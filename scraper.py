import requests
from bs4 import BeautifulSoup

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

    pub_list = []
    current_title = None
    current_cats = []

    for link in all_links:
        classes = link.get("class", [])
        
        # Title link
        if "link-white-to-secondary-20" in classes:
            # Save previous title + categories
            if current_title:
                pub_list.append([current_title, current_cats])
            current_title = link.get_text(strip=True)
            current_cats = []
        
        # Category link
        elif "font-size-90" in classes:
            current_cats.append(link.get_text(strip=True))
    
    # Add last title
    if current_title:
        pub_list.append([current_title, current_cats])
    return pub_list

def find_moods(results):
    pub_list = []
    for result in results:
        title = result[0]
        categories = result[1]
        for cat in categories:
            if 'Club' in cat or 'Bar' in cat:
                mood = 'party'
                break
            elif "Pub" in cat:
                mood = 'casual'
                break
        pub_list.append({"name": title, "mood": mood})
    return pub_list

def add_cat(pub_list,cat_list, cat_name):
    for i in range(len(pub_list)):
        pub_list[i][cat_name] = cat_list[i]
    return pub_list



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

def get_pub_scrape():
    pub_url = "https://www.designmynight.com/glasgow/bars/cool-and-quirky-bars-in-glasgow"
    prices = [ '££', '£', '£££', '£', '££', '£££', '£', '££', '£££', '£', '££', '£', '££', '££', '£', '££', '££', '£', '£', '££', '£', '£', '££', '£', '£', '£', '£', '£', '£']
    min_people = [4, 2, 5, 3, 4, 6, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 2, 4, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4]
    max_people = [10, 8, 12, 7, 10, 15, 6, 8, 12, 10, 7, 10, 5, 8, 10, 12, 6, 10, 7, 10, 5, 8, 10, 6, 8, 12, 6, 8, 10]

    events = pub_scrape_website(pub_url)
    pub_list = find_moods(events)
    pub_list = add_cat(pub_list, prices, "price")
    pub_list = add_cat(pub_list, min_people, "min")
    pub_list = add_cat(pub_list, max_people, "max")
    
    return pub_list

def get_event_scrape():
    event_url = "https://secretglasgow.com/things-to-do-october-glasgow/"
    events = event_scrape_website(event_url)
    return events