import re
import json
import random
import os

highlights_caches = {}
last_modified_times = {}


def process_highlights(txt_file_path, json_file_path):
    # * Read the txt file
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # * Split content by \n and remove empty lines
    lines = content.split("\n")
    lines = [line for line in lines if line.strip()]
    # * Determine the index of =======
    indices = [i for i, line in enumerate(lines) if "==========" in line]

    # * Pre-proceed the highlights
    pre_proceeded_highlights = []
    for i in range(len(indices)):
        if i == 0:
            pre_proceed_highlight = lines[:indices[i]]
        else:
            pre_proceed_highlight = lines[indices[i - 1]+1:indices[i]]

        # * If the highlight is less than 3 lines, skip it because that highlight is not complete
        if len(pre_proceed_highlight) < 3:
            continue

        pre_proceeded_highlights.append(pre_proceed_highlight)

    highlights = []

    pattern = r"^- Your (Highlight|Bookmark|Note) on (page [0-9]+ \| )?Location ([0-9]+(?:-[0-9]+)?) \| Added on (.*?)$"
    for highlight in pre_proceeded_highlights:
        match = re.findall(pattern, highlight[1], re.MULTILINE | re.DOTALL)
        book_title = highlight[0].strip()
        # book_type = match[0][0].strip()
        # page_info = match[0][1].strip() if match[0][1] else "N/A"
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

    # * Save highlights to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(highlights, json_file, indent=4, ensure_ascii=False)


def store_highlights(file_path, file_content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_content)


def store_and_process_highlights(message_id, file_content):
    os.makedirs(f"highlights/{message_id}", exist_ok=True)

    txt_file_path = f"highlights/{message_id}/original_highlights.txt"
    json_file_path = f"highlights/{message_id}/processed_highlights.json"

    store_highlights(txt_file_path, file_content)
    process_highlights(txt_file_path, json_file_path)


def load_random_highlight(message_id):
    global highlights_caches, last_modified_times

    json_file_path = f"highlights/{message_id}/processed_highlights.json"

    if not os.path.exists(json_file_path):
        return None

    current_modified_time = os.path.getmtime(json_file_path)
    last_modified_times = last_modified_times.get(message_id, 0)

    # * If the highlights are not cached or the file has been modified since the last cache then update the cache with the new highlights from the file
    if message_id not in highlights_caches or current_modified_time > last_modified_times:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            highlights_caches[message_id] = json.load(json_file)

        # * Update the last modified time
        last_modified_times[message_id] = current_modified_time

    # * Select a random highlight from the cached highlights
    random_highlight = random.choice(highlights_caches)
    return random_highlight


# * Helper function to format the highlights
def format_highlight(highlights):
    if highlights is None:
        return "No highlights found. Please import highlights first using /import."

    return (f"📚 *{highlights['book_title']}*"
            f"\n📍 Location: {highlights['location']}"
            f"\n🕒 Added on: {highlights['timestamp']}"
            f"\n\n{highlights['text']}")
