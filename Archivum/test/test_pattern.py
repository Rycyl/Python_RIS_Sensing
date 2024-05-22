import json
try:
    with open("RIS_patterns.json") as json_patterns:
        patterns_obj = json.load(json_patterns)
        patterns_data = patterns_obj["PATTERNS"]
        for pattern in patterns_data:
            print(pattern["DESC"])
except FileNotFoundError:
    print("File with patterns doesn't exist.")
    exit()
    