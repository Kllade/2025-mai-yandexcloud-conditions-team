import json

file_path = 'chat2024.json'
types = set()

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    for msg in data["messages"]:
        if msg["id"] == 82:
            break
        if msg["type"] == "message":
            for entity in msg["text_entities"]:
                entity_type = entity["type"]
                if entity_type not in types:
                    types.add(entity_type)
                    # print(f"{entity_type}:{entity["text"]}")

print(types)