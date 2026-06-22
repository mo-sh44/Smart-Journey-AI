import argparse
import os
import time

from dotenv import load_dotenv

from services.bluesky_service import BlueskyService


DEMO_POSTS = [
    (
        "Ich liebe mediterranes Essen, kleine Cafes und lokale Maerkte. "
        "Auf Reisen suche ich gern authentische Restaurants und entspannte Orte. "
        "#SmartJourneyAI #Travel"
    ),
    (
        "Museen, Architektur und historische Stadtviertel interessieren mich besonders. "
        "Eine gute Staedtereise braucht fuer mich Kultur, Spaziergaenge und gute Aussichtspunkte."
    ),
    (
        "Ich fotografiere gern schoene Strassen, Sonnenuntergaenge und besondere Aussichtspunkte. "
        "Bei Reisen sind Fotospots fuer mich ein wichtiger Teil der Planung."
    ),
    (
        "Ich mag warme Reiseziele, aber extreme Hitze ist fuer Sightseeing eher unpraktisch. "
        "Teilweise bewoelktes Wetter ist oft perfekt fuer eine Staedtereise."
    ),
    (
        "Bei Hotels achte ich auf gute Lage, faire Preise und kurze Wege zur Innenstadt. "
        "Fuer Barcelona waeren Cafes, Kultur und Strandnaehe spannend."
    ),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish the demo posts on the configured BlueSky account.",
    )
    args = parser.parse_args()

    load_dotenv()

    print("BlueSky demo post setup for Smart Journey AI")
    print()
    print(f"Configured account: {os.getenv('BLUESKY_USERNAME', 'not set')}")
    print()
    print("Prepared demo posts:")
    for index, post in enumerate(DEMO_POSTS, start=1):
        print(f"{index}. {post}")
    print()

    if not args.publish:
        print("Preview only. Nothing was published.")
        print("To publish these posts on the demo account, run:")
        print("python src/seed_bluesky_demo_posts.py --publish")
        return

    if not os.getenv("BLUESKY_USERNAME") or not os.getenv("BLUESKY_PASSWORD"):
        print("BlueSky credentials are missing.")
        print("Please set BLUESKY_USERNAME and BLUESKY_PASSWORD in .env.")
        return

    service = BlueskyService()
    for index, post in enumerate(DEMO_POSTS, start=1):
        print(f"Publishing post {index}/{len(DEMO_POSTS)}...")
        print(service.publish_post(post))
        time.sleep(2)

    print()
    print("Demo posts published. Now run:")
    print("python src/test_bluesky_source.py")
    print("python src/test_bluesky_personalization.py")


if __name__ == "__main__":
    main()
