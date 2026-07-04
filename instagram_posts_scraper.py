"""
Bright Data Instagram Posts Scraper

A Python wrapper for Bright Data's Instagram Posts scraper API.
Collect post data by URL or discover posts from profiles with filters.

Dataset ID: gd_lk5ns7kz21pck8jpis
Pricing: $0.0015/record
Avg Response Time: ~1s
"""

import os
import requests
from typing import List, Optional, Dict, Any, Union


class InstagramPostsScraper:
    """Client for the Bright Data Instagram Posts scraper API.

    Supports two collection modes:
    - collect_by_url: Fetch data for specific Instagram post URLs.
    - discover_by_profile: Discover posts from an Instagram profile with
      optional filters (date range, post type, count).
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
            "limit_per_input": limit_per_input,
        }

        params = {
            "dataset_id": self.DATASET_ID,
            "include_errors": "true",
        }

        return self._make_request(params, payload)

    def discover_by_profile(
        self,
        profiles: Union[str, Dict[str, Any], List[Dict[str, Any]]],
        limit_per_input: Optional[int] = None,
        # convenience kwargs when *profiles* is a plain URL string
        num_of_posts: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        post_type: Optional[str] = None,
        posts_to_not_include: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Discover posts from Instagram profiles with optional filters.

        Can be called in three ways:

        1. **Simple URL string** with keyword filters::

              scraper.discover_by_profile(
                  "https://www.instagram.com/natgeo",
                  num_of_posts=5,
                  start_date="01-01-2025",
                  end_date="03-01-2025",
                  post_type="Post",
              )

        2. **Single dict** with all fields::

              scraper.discover_by_profile({
                  "url": "https://www.instagram.com/natgeo",
                  "num_of_posts": 5,
              })

        3. **List of dicts** for batch collection::

              scraper.discover_by_profile([
                  {"url": "https://www.instagram.com/natgeo", "num_of_posts": 5},
                  {"url": "https://www.instagram.com/bbcnews", "num_of_posts": 3},
              ])

        Args:
            profiles: Profile URL string, a dict, or list of dicts.
            limit_per_input: Optional cap on records per input profile.
            num_of_posts: Number of posts to retrieve (convenience kwarg).
            start_date: Start date filter, format ``"MM-DD-YYYY"``.
            end_date: End date filter, format ``"MM-DD-YYYY"``.
            post_type: Filter by ``"Post"`` or ``"Reel"``.
            posts_to_not_include: List of post IDs to exclude.

        Returns:
            List of post data dictionaries.
        """
        if isinstance(profiles, str):
            profile_input = self._build_profile_dict(
                url=profiles,
                num_of_posts=num_of_posts,
                start_date=start_date,
                end_date=end_date,
                post_type=post_type,
                posts_to_not_include=posts_to_not_include,
            )
            input_list = [profile_input]
        elif isinstance(profiles, dict):
            input_list = [profiles]
        else:
            input_list = list(profiles)

        payload: Dict[str, Any] = {
            "input": input_list,
            "limit_per_input": limit_per_input,
        }

        params = {
            "dataset_id": self.DATASET_ID,
            "type": "discover_new",
            "discover_by": "url",
            "include_errors": "true",
        }

        return self._make_request(params, payload)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_profile_dict(
        url: str,
        num_of_posts: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        post_type: Optional[str] = None,
        posts_to_not_include: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Build a profile input dict, omitting ``None`` values."""
        entry: Dict[str, Any] = {"url": url}
        if num_of_posts is not None:
            entry["num_of_posts"] = num_of_posts
        if start_date is not None:
            entry["start_date"] = start_date
        if end_date is not None:
            entry["end_date"] = end_date
        if post_type is not None:
            entry["post_type"] = post_type
        if posts_to_not_include is not None:
            entry["posts_to_not_include"] = posts_to_not_include
        return entry

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
        )
        response.raise_for_status()
        return response.json()
