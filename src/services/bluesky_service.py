import os
import json
import requests
from datetime import datetime, timezone
from atproto import Client
from dotenv import load_dotenv

load_dotenv()


class BlueskyService:
    PDS_URL = "https://bsky.social"
    POSTS_CACHE_FILE = "./data/social_posts.json"

    def __init__(self):
        self.username = os.getenv("BLUESKY_USERNAME")
        self.password = os.getenv("BLUESKY_PASSWORD")

    def has_credentials(self) -> bool:
        return bool(self.username and self.password)

    def fetch_recent_posts(self, limit: int = 25) -> list:
        if not self.has_credentials():
            raise ValueError("BlueSky credentials are missing.")
        client = Client()
        client.login(self.username, self.password)
        profile = client.get_profile(actor=self.username)
        feed = client.get_author_feed(actor=profile.did, limit=limit)
        posts = [{"text": item.post.record.text, "created_at": item.post.record.created_at} for item in feed.feed]
        os.makedirs(os.path.dirname(self.POSTS_CACHE_FILE), exist_ok=True)
        with open(self.POSTS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        return posts

    def publish_post(self, text: str) -> str:
        try:
            if not self.has_credentials():
                return "Failed to publish: BlueSky credentials are missing."
            if len(text) > 300:
                text = text[:297] + "..."
            auth = requests.post(
                f"{self.PDS_URL}/xrpc/com.atproto.server.createSession",
                json={"identifier": self.username, "password": self.password},
                timeout=10,
            )
            auth.raise_for_status()
            session = auth.json()
            now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            pub = requests.post(
                f"{self.PDS_URL}/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {session['accessJwt']}"},
                json={
                    "repo": session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": {"$type": "app.bsky.feed.post", "text": text, "createdAt": now_iso},
                },
                timeout=10,
            )
            pub.raise_for_status()
            return "Post published on Bluesky."
        except Exception as exc:
            return f"Failed to publish: {exc}"
