import json
from typesafe_sdk import Choice, Noul, TypeSafeClient

nkpg = json.loads(open("nkpg.json", "r", encoding="utf-8").read())
orbi = json.loads(open("orbi.json", "r", encoding="utf-8").read())

events = nkpg + orbi

for event in events:
    client = TypeSafeClient(
        api_key = "YOUR_API_KEY",
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
            ),
            "requires_booking": Noul(
                instructions = "Does this event require booking or registration?",
            ),
            "restricted": Choice(
                instructions = "Are there any restrictions for who may attend this event?",
                criteria = {
                    "None": "There are no restrictions, the event is open for everyone",
                    "Students": "The event is open for all students",
                    "Other": "Any other restrictions",
                }
            )
        }
    )

    event["category"] = response.choices['category'].choice

    if event["requires_booking"] is None:
        if response.nouls['requires_booking'].noul >= 0.5:
            event["requires_booking"] = True
        else:
            event["requires_booking"] = False

    if response.choices["restricted"].choice == "Other":
        event["restricted"] = True
    else:
        event["restricted"] = False

json.dump(events, open("events.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
