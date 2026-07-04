# Bright Data Instagram Posts Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

A Python wrapper for [Bright Data's Instagram Posts scraper API](https://get.brightdata.com/1tndi4600b25). Collect detailed post data by URL or discover posts from any public profile with date, type, and count filters.

## Features

- **Collect by URL** - Fetch full post data from one or more Instagram post URLs
- **Discover by Profile** - Discover posts from any profile with date range, post type, and count filters
- **Batch support** - Process multiple URLs or profiles in a single API call
- **40 data fields** - Likes, comments, hashtags, location, media URLs, tagged profiles, and more
- **Simple interface** - Clean Pythonic API with type hints
- **Fast** - Average response time of ~1 second

## Prerequisites

- Python 3.8 or higher
- A Bright Data account with API access - [Sign up here](https://get.brightdata.com/1tndi4600b25)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/luminati-io/bright-data-instagram-posts-scraper.git
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

# Discover posts from a profile
results = scraper.discover_by_profile(
    "https://www.instagram.com/natgeo",
    num_of_posts=10,
    start_date="01-01-2025",
    end_date="03-01-2025",
    post_type="Post",
)
for post in results:
    print(f"{post['url']} - {post['likes']} likes")
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

---

### `discover_by_profile(profiles, limit_per_input=None, **kwargs)`

Discover posts from Instagram profiles with optional filters. Supports three calling conventions.

#### Option 1: URL string with keyword arguments

| Parameter              | Type         | Required | Description                                     |
|------------------------|--------------|----------|-------------------------------------------------|
| `profiles`             | `str`        | Yes      | Instagram profile URL                           |
| `num_of_posts`         | `int`        | No       | Number of posts to retrieve                     |
| `start_date`           | `str`        | No       | Start date filter (`"MM-DD-YYYY"`)              |
| `end_date`             | `str`        | No       | End date filter (`"MM-DD-YYYY"`)                |
| `post_type`            | `str`        | No       | `"Post"` or `"Reel"`                            |
| `posts_to_not_include` | `list[str]`  | No       | List of post IDs to exclude                     |
| `limit_per_input`      | `int`        | No       | Max records per input profile                   |

```python
results = scraper.discover_by_profile(
    "https://www.instagram.com/natgeo",
    num_of_posts=10,
    start_date="01-01-2025",
    end_date="03-01-2025",
    post_type="Post",
)
```

#### Option 2: Single dict

```python
results = scraper.discover_by_profile({
    "url": "https://www.instagram.com/natgeo",
    "num_of_posts": 10,
    "start_date": "01-01-2025",
    "end_date": "03-01-2025",
    "post_type": "Post",
})
```

#### Option 3: List of dicts (batch)

```python
results = scraper.discover_by_profile([
    {"url": "https://www.instagram.com/natgeo", "num_of_posts": 5},
    {"url": "https://www.instagram.com/bbcnews", "num_of_posts": 3, "post_type": "Reel"},
])
```

**Returns:** `list[dict]` - List of post data dictionaries.

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
    "user_posted": "natgeo",
    "description": "A stunning view of the Northern Lights captured from Iceland.",
    "hashtags": ["nature", "northernlights", "iceland", "travel"],
    "num_comments": 342,
    "date_posted": "2024-01-15T18:30:00.000Z",
    "likes": 125000,
    "photos": [
        "https://scontent.cdninstagram.com/v/photo1.jpg",
        "https://scontent.cdninstagram.com/v/photo2.jpg"
    ],
    "videos": [],
    "location": "Reykjavik, Iceland",
    "tagged_profiles": ["photographer_jane"],
    "is_video": false,
    "is_sponsored": false
}
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why Bright Data?

[Bright Data](https://get.brightdata.com/1tndi4600b25) provides the most reliable infrastructure for web data collection:

- **Pre-built scrapers** - No need to build or maintain scraping logic
- **Structured data** - Clean JSON output with 40+ fields per post
- **High success rate** - Built-in proxy rotation and anti-blocking
- **Scalable** - Handle thousands of requests with consistent performance
- **Compliant** - Ethical data collection with full regulatory compliance
- **Pay per result** - Only $0.0015 per record with no upfront costs

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclosure:** Some links in this document are affiliate links. If you sign up for Bright Data through these links, I may earn a commission at no extra cost to you. This helps support the maintenance of this project.
