# 代码生成时间: 2025-08-19 22:19:54
# Import necessary libraries
import requests
from celery import Celery
from urllib.parse import urlparse

# Define the Celery app
app = Celery('url_validator', broker='pyamqp://guest@localhost//')

# Define the URL validation task
@app.task
def validate_url(url):
    """
    Validates the URL by checking if it is reachable and has a valid scheme.
    
    Args:
    url (str): The URL to be validated.
    
    Returns:
    dict: A dictionary containing the validation result and status message.
    """
    try:
        # Parse the URL to check for a valid scheme
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return {'valid': False, 'message': 'Invalid URL scheme'}
        
        # Send a HEAD request to check if the URL is reachable
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return {'valid': True, 'message': 'URL is valid'}
        else:
            return {'valid': False, 'message': f'URL is not reachable, status code: {response.status_code}'}
    except requests.exceptions.RequestException as e:
        return {'valid': False, 'message': f'Error validating URL: {str(e)}'}
    except Exception as e:
        return {'valid': False, 'message': f'An unexpected error occurred: {str(e)}'}
