# 代码生成时间: 2025-08-15 11:25:51
import requests
from celery import Celery
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Celery configuration
app = Celery('web_content_scraper', broker='pyamqp://guest@localhost//')

# Define a function to fetch web content
@app.task
def fetch_web_content(url):
    """
    Fetches the content of a webpage and returns it as a string.
    
    :param url: The URL of the webpage to fetch.
    :return: The content of the webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

# Define a function to parse and extract content from HTML
def parse_html(html_content):
    """
    Parses the HTML content and extracts relevant information.
    
    :param html_content: The HTML content of the webpage.
    :return: A dictionary with extracted information.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Example of extracting the title of the webpage
    title = soup.find('title').get_text() if soup.find('title') else None
    return {'title': title}

# Define a function to scrape content from a webpage
@app.task
def scrape_webpage(url):
    """
    Scrapes the content from a webpage by fetching and parsing it.
    
    :param url: The URL of the webpage to scrape.
    :return: A dictionary with the extracted information.
    """
    html_content = fetch_web_content(url)
    if html_content:
        return parse_html(html_content)
    else:
        return None

# Example usage
if __name__ == '__main__':
    # Replace 'http://example.com' with the URL you want to scrape
    url_to_scrape = 'http://example.com'
    result = scrape_webpage.delay(url_to_scrape)
    print(f"Scraping result: {result.get()}")