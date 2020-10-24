"""Get random encounters"""

import json
import random

with open("social_encounters.json") as json_file:
    social_encounters = json.load(json_file)

def select_encounter():
    unused_encounters = social_encounters.get("unused")
    if not unused_encounters:
        return "No unused encounters left"
    selected_encounter = social_encounters.get("selected")
    temp_select = unused_encounters.pop(random.randint(0, len(unused_encounters)-1))
    if selected_encounter:
        unused_encounters.extend(selected_encounter)
    selected_encounter = [temp_select]
    social_encounters["selected"] = selected_encounter
    social_encounters["unused"] = unused_encounters
    with open("social_encounters.json", 'w') as f:
        json.dump(social_encounters, f, indent=4)
    return selected_encounter[0]

def use_encounter():
    selected_encounter = social_encounters.get("selected")
    if not selected_encounter:
        return "No encouter selected"
    used_encounters = social_encounters.get("used")
    used_encounters.extend(selected_encounter)
    selected_encounter.pop()
    social_encounters["selected"] = selected_encounter
    social_encounters["used"] = used_encounters
    with open("social_encounters.json", 'w') as f:
        json.dump(social_encounters, f, indent=4)
    return "Encounter used!"


