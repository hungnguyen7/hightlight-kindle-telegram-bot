import re
import json
import random
import os

highlights_cache = None
last_modified_time = None


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
    global highlights_cache, last_modified_time

    json_file_path = "highlights.json"

    if not os.path.exists(json_file_path):
        return None

    # Get the last modified time of the file
    current_modified_time = os.path.getmtime(json_file_path)

    # If cache is empty or the file has been modified since the last load, reload the file
    if highlights_cache is None or current_modified_time != last_modified_time:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            highlights_cache = json.load(json_file)

        # Update the last modified time
        last_modified_time = current_modified_time

    # Select a random highlight from the cached highlights
    random_highlight = random.choice(highlights_cache)
    return random_highlight
