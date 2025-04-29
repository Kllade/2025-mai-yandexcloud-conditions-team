import json, emoji

def pars(path_in: str, path_out: str):
    bad_types = {'pre', 'custom_emoji', 'bot_command', 'link', 'mention_name', 'mention', 'code', 'hashtag', 'blockquote', 'phone'}
    res = []

    with open(path_in, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for msg in data["messages"]:
        if msg["type"] != "message":
            continue
        if len(msg["text_entities"]) == 0:
            continue
        cur_msg = ''
        for entity in msg["text_entities"]:
            if entity["type"] not in bad_types:
                cur_msg += entity["text"]
        cur_msg = cur_msg.strip()
        cur_msg = ''.join([c for c in cur_msg if not emoji.is_emoji(c)])
        if cur_msg == '':
            continue
        if "reply_to_message_id" in msg and msg["reply_to_message_id"] >= 81:
            res.append({"id": msg["id"], "reply_to_message_id": msg["reply_to_message_id"], "text": cur_msg})
        else:
            res.append({"id": msg["id"], "text": cur_msg})

    with open(path_out, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2, ensure_ascii=False)

for p in range(2021, 2025):
    pars(f"chat{p}.json", f"data{p}.json")