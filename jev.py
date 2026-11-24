import json
from typesafe_sdk import Choice, Noul, TypeSafeClient

events = json.loads(open("nkpg.json", "r", encoding="utf-8").read())

for event in events:
    client = TypeSafeClient(
        api_key="YOUR_API_KEY",
    )
    response = client.system_one(
        state = event["summary"],
        questions = {
            "category": Choice(
                instructions = "What type of event is this?",
                criteria = {
                    "Music": "A musical performance or concert",
                    "Art": "An art exhibition or workshop",
                    "Theater": "A theater performance or play",
                    "Sports": "A sports event or competition",
                    "Party": "A social gathering or party",
                    "Professional": "A professional development event",
                    "Networking": "A networking event",
                    "Family": "A family-friendly event",
                    "Learning": "An educational or learning event",
                    }
            )
        }
    )

    print(f"Event: {event['title']}")
    print(f"Category: {response.choices["category"].choice}")
    print()