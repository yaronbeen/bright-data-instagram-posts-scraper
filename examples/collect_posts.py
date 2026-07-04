"""
Example: Collect Instagram Posts by URL

Fetches post data for specific Instagram post URLs using the
Bright Data Instagram Posts scraper.

Usage:
    export BRIGHT_DATA_API_TOKEN="your_api_token_here"
    python examples/collect_posts.py
"""

from instagram_posts_scraper import InstagramPostsScraper


def main():
    scraper = InstagramPostsScraper()

    # --- Single post ---
    print("=== Collecting a single post ===")
    results = scraper.collect_by_url(
        "https://www.instagram.com/p/Cuf4s0MNqNr"
    )
    for post in results:
        print(f"  URL:   {post.get('url')}")
        print(f"  User:  {post.get('user_posted')}")
        print(f"  Likes: {post.get('likes')}")
        print(f"  Date:  {post.get('date_posted')}")
        print()

    # --- Multiple posts ---
    print("=== Collecting multiple posts ===")
    results = scraper.collect_by_url([
        "https://www.instagram.com/p/Cuf4s0MNqNr",
        "https://www.instagram.com/p/DP861NijuwE",
    ])
    for post in results:
        print(f"  URL:         {post.get('url')}")
        print(f"  User:        {post.get('user_posted')}")
        print(f"  Description: {post.get('description', '')[:80]}...")
        print(f"  Likes:       {post.get('likes')}")
        print(f"  Comments:    {post.get('num_comments')}")
        print(f"  Is Video:    {post.get('is_video')}")
        print(f"  Sponsored:   {post.get('is_sponsored')}")
        print()


if __name__ == "__main__":
    main()
