"""
Example: Discover Instagram Posts by Profile

Discovers posts from Instagram profiles with optional date range,
post type, and count filters.

Usage:
    export BRIGHT_DATA_API_TOKEN="your_api_token_here"
    python examples/discover_posts_by_profile.py
"""

from instagram_posts_scraper import InstagramPostsScraper


def main():
    scraper = InstagramPostsScraper()

    # --- Simple: discover recent posts from a profile ---
    print("=== Discover posts from a profile (simple) ===")
    results = scraper.discover_by_profile(
        "https://www.instagram.com/natgeo",
        num_of_posts=5,
    )
    for post in results:
        print(f"  URL:   {post.get('url')}")
        print(f"  Date:  {post.get('date_posted')}")
        print(f"  Likes: {post.get('likes')}")
        print()

    # --- With date range and post type filter ---
    print("=== Discover posts with date range + type filter ===")
    results = scraper.discover_by_profile(
        "https://www.instagram.com/marcusfaberfdp",
        num_of_posts=10,
        start_date="01-01-2025",
        end_date="03-01-2025",
        post_type="Post",
    )
    for post in results:
        print(f"  URL:      {post.get('url')}")
        print(f"  Date:     {post.get('date_posted')}")
        print(f"  Likes:    {post.get('likes')}")
        print(f"  Hashtags: {post.get('hashtags')}")
        print()

    # --- Batch: multiple profiles at once ---
    print("=== Batch discover from multiple profiles ===")
    results = scraper.discover_by_profile([
        {
            "url": "https://www.instagram.com/natgeo",
            "num_of_posts": 3,
            "post_type": "Reel",
        },
        {
            "url": "https://www.instagram.com/bbcnews",
            "num_of_posts": 3,
            "start_date": "01-01-2025",
            "end_date": "06-01-2025",
        },
    ])
    for post in results:
        print(f"  URL:      {post.get('url')}")
        print(f"  User:     {post.get('user_posted')}")
        print(f"  Likes:    {post.get('likes')}")
        print(f"  Location: {post.get('location')}")
        print()

    # --- Excluding specific posts ---
    print("=== Discover posts while excluding specific post IDs ===")
    results = scraper.discover_by_profile(
        "https://www.instagram.com/natgeo",
        num_of_posts=5,
        posts_to_not_include=["Cuf4s0MNqNr", "DP861NijuwE"],
    )
    for post in results:
        print(f"  URL:   {post.get('url')}")
        print(f"  Likes: {post.get('likes')}")
        print()


if __name__ == "__main__":
    main()
