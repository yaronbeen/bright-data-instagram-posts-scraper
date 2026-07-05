# Bright Data Instagram Posts Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

A Python wrapper for Bright Data's Instagram Posts scraper API. Collect detailed post data by providing specific Instagram post URLs.

> **All Instagram scrapers:** [Profile Scraper](https://github.com/yaronbeen/bright-data-instagram-profile-scraper) · [Profile Discovery](https://github.com/yaronbeen/bright-data-instagram-profile-discovery) · **Posts Scraper** · [Posts Discovery](https://github.com/yaronbeen/bright-data-instagram-posts-discovery) · [Reels Scraper](https://github.com/yaronbeen/bright-data-instagram-reels-scraper) · [Reels Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-discovery) · [Reels (All) Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-all-discovery) · [Comments Scraper](https://github.com/yaronbeen/bright-data-instagram-comments-scraper)

## Features

- **Collect by URL** - Fetch full post data from one or more Instagram post URLs
- **Batch support** - Process multiple URLs in a single API call
- **40 data fields** - Likes, comments, hashtags, location, media URLs, tagged profiles, and more
- **Simple interface** - Clean Pythonic API with type hints
- **Fast** - Average response time of ~1 second

## Use Cases

- Analyze which content types get the most engagement
- Track hashtag performance across posts
- Monitor competitor posting frequency and strategy
- Collect media URLs for content research

## Prerequisites

- Python 3.8 or higher
- A Bright Data account with API access (create an account at https://brightdata.com)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yaronbeen/bright-data-instagram-posts-scraper.git
cd bright-data-instagram-posts-scraper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API token:

```bash
cp .env.example .env
# Edit .env and add your Bright Data API token
```

Or export it directly:

```bash
export BRIGHT_DATA_API_TOKEN="your_api_token_here"
```

## Quick Start

```python
from instagram_posts_scraper import InstagramPostsScraper

scraper = InstagramPostsScraper()

# Collect a specific post
results = scraper.collect_by_url("https://www.instagram.com/p/Cuf4s0MNqNr")
for post in results:
    print(f"{post['user_posted']}: {post['likes']} likes")
```

## API Reference

### `InstagramPostsScraper(api_token=None)`

Create a scraper instance.

| Parameter   | Type            | Required | Description                                                                 |
|-------------|-----------------|----------|-----------------------------------------------------------------------------|
| `api_token` | `str` or `None` | No       | Bright Data API token. Falls back to `BRIGHT_DATA_API_TOKEN` env variable. |

---

### `collect_by_url(urls, limit_per_input=None)`

Collect post data from specific Instagram post URLs.

| Parameter         | Type               | Required | Description                                      |
|-------------------|--------------------|----------|--------------------------------------------------|
| `urls`            | `str` or `list`    | Yes      | Single URL string or list of Instagram post URLs |
| `limit_per_input` | `int` or `None`    | No       | Max records to return per input URL              |

**Returns:** `list[dict]` - List of post data dictionaries.

**Example:**

```python
# Single post
results = scraper.collect_by_url("https://www.instagram.com/p/Cuf4s0MNqNr")

# Multiple posts
results = scraper.collect_by_url([
    "https://www.instagram.com/p/Cuf4s0MNqNr",
    "https://www.instagram.com/p/DP861NijuwE",
])
```

## Output Fields

Each post record contains up to 40 fields. Key fields include:

| Field              | Type     | Description                        |
|--------------------|----------|------------------------------------|
| `url`              | `str`    | Post URL                          |
| `user_posted`      | `str`    | Username of the poster            |
| `description`      | `str`    | Post caption / description        |
| `hashtags`         | `list`   | List of hashtags                  |
| `num_comments`     | `int`    | Number of comments                |
| `date_posted`      | `str`    | ISO 8601 timestamp                |
| `likes`            | `int`    | Number of likes                   |
| `photos`           | `list`   | List of photo URLs                |
| `videos`           | `list`   | List of video URLs                |
| `location`         | `str`    | Tagged location                   |
| `tagged_profiles`  | `list`   | List of tagged usernames          |
| `is_video`         | `bool`   | Whether the post is a video       |
| `is_sponsored`     | `bool`   | Whether the post is sponsored     |

## Example Output

```json
{
    "url": "https://www.instagram.com/p/Cuf4s0MNqNr",
    "user_posted": "thebucketlistfamily",
    "description": "Morning light hitting the rice terraces just right. Moments like these remind us why we travel slow.",
    "hashtags": ["slowtravel", "familytravel", "bali", "riceterraces"],
    "num_comments": 87,
    "date_posted": "2024-01-15T18:30:00.000Z",
    "likes": 4832,
    "photos": [
        "https://scontent.cdninstagram.com/v/t51.2885-15/photo1.jpg",
        "https://scontent.cdninstagram.com/v/t51.2885-15/photo2.jpg"
    ],
    "videos": [],
    "location": "Ubud, Bali",
    "tagged_profiles": ["visitbali"],
    "is_video": false,
    "is_sponsored": false
}
```

> Note: This is a representative example. Actual field values and available fields may vary.

## Error Handling

The scraper raises standard exceptions you can catch:

```python
import requests
from instagram_posts_scraper import InstagramPostsScraper

try:
    scraper = InstagramPostsScraper()
    results = scraper.collect_by_url("https://www.instagram.com/p/Cuf4s0MNqNr")
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API")
```

| Exception                          | Cause                                  |
|------------------------------------|----------------------------------------|
| `ValueError`                       | Missing API token.                     |
| `requests.exceptions.HTTPError`    | API returned 4xx/5xx (auth, rate limit, etc.). |
| `requests.exceptions.ConnectionError` | Network connectivity issue.         |
| `requests.exceptions.ReadTimeout`  | Request took longer than 30 seconds.   |

## Rate Limits

- **Sync mode:** Results returned directly in the response. Best for small batches (1-10 inputs).
- **Async mode:** For larger jobs, use the async API. See [Bright Data API docs](https://docs.brightdata.com/datasets/functions/introduction).
- **No hard rate limit** on API calls, but performance varies with batch size.
- **Pricing:** $0.0015 per record ($1.50 per 1,000 records).

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why Bright Data?

Instagram post data is rich but heavily protected. Bright Data gives you the full picture without the infrastructure headaches:

- **40 fields per post** - Media URLs, location, tagged profiles, sponsorship status, and more in structured JSON
- **Anti-scraping handled automatically** - Proxy rotation, fingerprinting, and rate limit management built in
- **Batch multiple post URLs** in a single API call for efficient collection
- **$0.0015/record** - Cheaper than building and maintaining your own scraping infrastructure
- **High success rate** - Consistent data delivery even as Instagram changes its anti-bot measures

For full API documentation, see the [Bright Data API Reference](https://docs.brightdata.com/datasets/functions/introduction).

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclosure:** Some links in this document are affiliate links. If you sign up for Bright Data through these links, I may earn a commission at no extra cost to you. This helps support the maintenance of this project.
