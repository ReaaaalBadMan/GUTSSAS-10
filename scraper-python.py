import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        print("goat")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}") 
        return

if __name__ == "__main__":
    url = "https://secretglasgow.com/things-to-do-october-glasgow/"
    scrape_website(url)