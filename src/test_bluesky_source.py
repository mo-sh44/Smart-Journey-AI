import os

from dotenv import load_dotenv
from services.bluesky_service import BlueskyService


def main():
    load_dotenv()

    if not os.getenv("BLUESKY_USERNAME") or not os.getenv("BLUESKY_PASSWORD"):
        print("BlueSky credentials are missing.")
        print("Please set BLUESKY_USERNAME and BLUESKY_PASSWORD in .env.")
        return

    print("Testing BlueSky data source for Smart Journey AI")
    print("Action: fetch recent posts only")
    print()

    posts = BlueskyService().fetch_recent_posts(limit=3)

    print("BlueSky source works.")
    print(f"Fetched posts: {len(posts)}")
    for index, post in enumerate(posts, start=1):
        text = post.get("text", "").replace("\n", " ")
        if len(text) > 120:
            text = text[:117] + "..."
        print(f"{index}. {text}")

    print()
    print("Note: This test only reads recent posts. It does not publish anything.")


if __name__ == "__main__":
    main()
