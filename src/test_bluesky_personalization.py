import os

from dotenv import load_dotenv

from services.bluesky_service import BlueskyService


INTEREST_KEYWORDS = {
    "Kultur und Museen": ["museum", "museen", "kunst", "kultur", "galerie", "architecture", "architektur"],
    "Cafes und lokales Essen": ["cafe", "café", "kaffee", "restaurant", "tapas", "essen", "food"],
    "Strand und Entspannung": ["strand", "beach", "meer", "sonne", "entspannung", "relax"],
    "Fotografie und Aussichtspunkte": ["foto", "fotografie", "photos", "kamera", "aussicht", "view"],
    "Outdoor und Aktivitaeten": ["wandern", "hiking", "outdoor", "park", "sport", "walking"],
}


def detect_interests(posts):
    combined_text = " ".join(post.get("text", "") for post in posts).lower()
    detected = []
    for interest, keywords in INTEREST_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            detected.append(interest)
    return detected


def main():
    load_dotenv()

    if not os.getenv("BLUESKY_USERNAME") or not os.getenv("BLUESKY_PASSWORD"):
        print("BlueSky credentials are missing.")
        print("Please set BLUESKY_USERNAME and BLUESKY_PASSWORD in .env.")
        return

    print("Testing BlueSky personalization for Smart Journey AI")
    print("Action: fetch recent posts and derive travel interests")
    print()

    posts = BlueskyService().fetch_recent_posts(limit=10)
    if not posts:
        print("No BlueSky posts found.")
        print("Add a few demo posts to the BlueSky account and run this test again.")
        return

    interests = detect_interests(posts)

    print(f"Fetched posts: {len(posts)}")
    print()
    print("Detected interests:")
    if interests:
        for interest in interests:
            print(f"- {interest}")
    else:
        print("- No clear travel interests detected yet")

    print()
    print("How Smart Journey AI uses this:")
    if interests:
        print("For Barcelona, the assistant should prioritize:")
        if "Kultur und Museen" in interests:
            print("- Gothic Quarter, Picasso Museum, architecture-focused sightseeing")
        if "Cafes und lokales Essen" in interests:
            print("- tapas restaurants, local cafes, market visits")
        if "Strand und Entspannung" in interests:
            print("- beach time and relaxed hotel options")
        if "Fotografie und Aussichtspunkte" in interests:
            print("- Bunkers del Carmel and scenic photo spots")
        if "Outdoor und Aktivitaeten" in interests:
            print("- parks, walking routes, outdoor activities")
    else:
        print("The assistant can still plan the trip, but personalization is weaker.")

    print()
    print("Note: This test only reads posts. It does not publish anything.")


if __name__ == "__main__":
    main()
