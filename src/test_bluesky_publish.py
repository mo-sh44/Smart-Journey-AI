import argparse
import os

from dotenv import load_dotenv

from services.bluesky_service import BlueskyService


DEMO_POST = (
    "Planning a personalized Barcelona trip with Smart Journey AI: "
    "weather checked, flights and hotels compared, and the itinerary adapted "
    "to culture, cafes, and photo spots. #SmartJourneyAI #Travel"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Actually publish the demo post on BlueSky.",
    )
    args = parser.parse_args()

    load_dotenv()

    print("Testing BlueSky publishing for Smart Journey AI")
    print()
    print("Prepared demo post:")
    print(DEMO_POST)
    print()

    if not args.publish:
        print("Preview only. Nothing was published.")
        print("To publish this post on the demo account, run:")
        print("python src/test_bluesky_publish.py --publish")
        return

    if not os.getenv("BLUESKY_USERNAME") or not os.getenv("BLUESKY_PASSWORD"):
        print("BlueSky credentials are missing.")
        print("Please set BLUESKY_USERNAME and BLUESKY_PASSWORD in .env.")
        return

    result = BlueskyService().publish_post(DEMO_POST)
    print(result)


if __name__ == "__main__":
    main()
