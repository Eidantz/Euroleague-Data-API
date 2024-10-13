import requests
from typing import Dict, Any, Optional

EUROLEAGUE_API_URL_V3 = "https://api-live.euroleague.net/v3"
EUROLEAGUE_API_URL_V2 = "https://api-live.euroleague.net/v2"

def make_euroleague_request_v3(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Makes a request to the Euroleague API and returns the response data.
    
    Args:
        endpoint (str): The API endpoint (e.g., '/clubs').
        params (Optional[Dict[str, Any]]): The query parameters to include in the request.
    
    Returns:
        Dict[str, Any]: The JSON response data from the API.
    """
    url = f"{EUROLEAGUE_API_URL_V3}/{endpoint}"
    # remove all None values from the params
    params = {k: v for k, v in (params or {}).items() if v is not None}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while making request to {url}: {e}")
        return {}

def make_euroleague_request_v2(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Makes a request to the Euroleague API and returns the response data.
    
    Args:
        endpoint (str): The API endpoint (e.g., '/clubs').
        params (Optional[Dict[str, Any]]): The query parameters to include in the request.
    
    Returns:
        Dict[str, Any]: The JSON response data from the API.
    """
    url = f"{EUROLEAGUE_API_URL_V2}/{endpoint}"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while making request to {url}: {e}")
        return {}
