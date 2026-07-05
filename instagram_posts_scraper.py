"""
Bright Data Instagram Posts Scraper

A Python wrapper for Bright Data's Instagram Posts scraper API.
Collect post data by providing specific Instagram post URLs.

Dataset ID: gd_lk5ns7kz21pck8jpis
Pricing: $0.0015/record
Avg Response Time: ~1s
"""

import os
import requests
from typing import List, Optional, Dict, Any, Union


class InstagramPostsScraper:
    """Client for the Bright Data Instagram Posts scraper API.

    Collects post data for specific Instagram post URLs.
    """

    BASE_URL = "https://api.brightdata.com/datasets/v3/scrape"
    DATASET_ID = "gd_lk5ns7kz21pck8jpis"

    def __init__(self, api_token: Optional[str] = None):
        """Initialize the scraper with a Bright Data API token.

        Args:
            api_token: Bright Data API token. If not provided, reads from
                       the BRIGHT_DATA_API_TOKEN environment variable.

        Raises:
            ValueError: If no API token is provided or found in env.
        """
        self.api_token = api_token or os.getenv("BRIGHT_DATA_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "API token is required. Pass it directly or set the "
                "BRIGHT_DATA_API_TOKEN environment variable."
            )

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def collect_by_url(
        self,
        urls: Union[str, List[str]],
        limit_per_input: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Collect post data from specific Instagram post URLs.

        Args:
            urls: A single Instagram post URL string or a list of URLs.
                  Example: "https://www.instagram.com/p/Cuf4s0MNqNr"
            limit_per_input: Optional cap on records returned per input URL.

        Returns:
            List of post data dictionaries.
        """
        if isinstance(urls, str):
            urls = [urls]

        payload: Dict[str, Any] = {
            "input": [{"url": url} for url in urls],
        }
        if limit_per_input is not None:
            payload["limit_per_input"] = limit_per_input

        params = {
            "dataset_id": self.DATASET_ID,
            "include_errors": "true",
        }

        return self._make_request(params, payload)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _make_request(
        self,
        params: Dict[str, str],
        payload: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Send a POST request to the Bright Data scraper API.

        Args:
            params: URL query parameters.
            payload: JSON body.

        Returns:
            Parsed JSON response (list of dicts).

        Raises:
            requests.exceptions.HTTPError: On 4xx / 5xx responses.
            requests.exceptions.RequestException: On connection failures.
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            params=params,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
