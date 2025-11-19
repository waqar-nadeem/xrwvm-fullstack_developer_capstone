import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    "backend_url",
    default="https://nadeemwaqar2-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/"
)
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    default="http://localhost:5050/"
)

def get_request(endpoint, **kwargs):
    """Send GET request to backend and return JSON"""
    # Ensure endpoint ends with /
    if not endpoint.endswith("/"):
        endpoint += "/"

    request_url = backend_url + endpoint

    if kwargs:
        request_url += "?"
        request_url += "&".join([f"{k}={v}" for k, v in kwargs.items()])

    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()  # raise error on HTTP codes != 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception: {e}")
        return None
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return None

def analyze_review_sentiments(text):
    url = sentiment_analyzer_url
    if not url.endswith("/"):
        url += "/"
    request_url = url + "analyze/" + text

    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception: {e}")
        return None
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return None

def post_review(data_dict):
    request_url = backend_url
    if not request_url.endswith("/"):
        request_url += "/"
    request_url += "insert_review"

    try:
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception: {e}")
        return None
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return None
