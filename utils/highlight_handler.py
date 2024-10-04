import re
import json
import random
import os


def process_and_store_highlights():
    # Read the txt file
    with open("highlights.txt", 'r', encoding='utf-8') as file:
        content = file.read()

    # Split content by \n and remove empty lines
    lines = content.split("\n")
    lines = [line for line in lines if line.strip()]
    # Determine the index of =======
    indices = [i for i, line in enumerate(lines) if "==========" in line]

    # Pre-proceed the highlights
    pre_proceeded_highlights = []
    for i in range(len(indices)):
        if i == 0:
            pre_proceed_highlight = lines[:indices[i]]
        else:
            pre_proceed_highlight = lines[indices[i - 1]+1:indices[i]]

        # If the highlight is less than 3 lines, skip it because that highlight is not complete
        if len(pre_proceed_highlight) < 3:
            continue

        pre_proceeded_highlights.append(pre_proceed_highlight)

    highlights = []
    # Adjusted regular expression to cover different cases
    pattern = r"^- Your (Highlight|Bookmark|Note) on (page [0-9]+ \| )?Location ([0-9]+(?:-[0-9]+)?) \| Added on (.*?)$"
    for highlight in pre_proceeded_highlights:
        match = re.findall(pattern, highlight[1], re.MULTILINE | re.DOTALL)
        book_title = highlight[0].strip()
        book_type = match[0][0].strip()
        page_info = match[0][1].strip() if match[0][1] else "N/A"
        location = match[0][2].strip()
        timestamp = match[0][3].strip()
        text = highlight[2].strip()
        highlights.append({
            "book_title": book_title,
            # "type": book_type,
            # "page_info": page_info,
            "location": location,
            "timestamp": timestamp,
            "text": text
        })

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


if __name__ == "__main__":
    process_and_store_highlights()
