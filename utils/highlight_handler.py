import re
import json
import random
import os


def process_and_store_highlights():
    # Read the txt file
    with open("highlights.txt", 'r', encoding='utf-8') as file:
        content = file.read()

    # Adjusted regular expression to cover different cases
    pattern = r"^(.*?)\n- Your (Highlight|Bookmark) on (page [0-9]+ \| )?Location ([0-9]+(?:-[0-9]+)?) \| Added on (.*?)\n\n(.*?)\n==========$"
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    highlights = []
    for match in matches:
        book_title = match[0].strip()
        item_type = match[1].strip()  # 'Highlight' or 'Bookmark'
        # Handle missing page information
        page_info = match[2].strip() if match[2] else "N/A"
        location = match[3].strip()
        timestamp = match[4].strip()
        text = match[5].strip()

        highlights.append({
            "book_title": book_title,
            "type": item_type,
            "page_info": page_info,
            "location": location,
            "timestamp": timestamp,
            "text": text
        })

    # Remove all highlights where text is empty
    highlights = [highlight for highlight in highlights if highlight["text"]]

    # Save highlights to a JSON file
    with open("highlights.json", 'w', encoding='utf-8') as json_file:
        json.dump(highlights, json_file, indent=4, ensure_ascii=False)


def load_random_highlight():

    if not os.path.exists("highlights.json"):
        return None

    # Load the stored highlights from the JSON file
    with open("highlights.json", 'r', encoding='utf-8') as json_file:
        highlights = json.load(json_file)

    # Select a random highlight
    random_highlight = random.choice(highlights)

    return random_highlight
