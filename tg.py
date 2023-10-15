import json
import time
from datetime import datetime

import openai
from telethon import TelegramClient

from config import *

AI = False
limit = 500
offset = 30
tgID = "rozetked"
modelName = 'text-davinci-002'

client = TelegramClient('tg_parcer', api_id, api_hash)
openai.api_key = api_key


def get_tags(text):
    """Retrieve tags for a given text using OpenAI API."""
    if not AI:
        return "-"

    response = openai.Completion.create(
        engine=modelName,
        prompt=f"print one hashtag that describes the text as accurately as possible:\n\n{text}",
        max_tokens=5
    )
    return response.choices[0].text.strip()


def normalize_array(sum_array):
    """Normalize the total reactions to a range between 0 and 1."""
    min_count = min(sum_array)
    max_count = max(sum_array)

    if min_count == max_count:
        return sum_array

    normalized_counts = []
    for x in sum_array:
        normalized_x = (x - min_count) / (max_count - min_count)
        normalized_counts.append(normalized_x)

    return normalized_counts


def standardize_array(sum_array):
    """Standardize the array to have mean 0 and standard deviation 1."""

    mean_value = sum(sum_array) / len(sum_array)
    std_dev = (sum([(x - mean_value) ** 2 for x in sum_array]) / len(sum_array)) ** 0.5

    # If standard deviation is zero, return the original array to avoid division by zero
    if std_dev == 0:
        return sum_array

    standardized_counts = [(x - mean_value) / std_dev for x in sum_array]

    return standardized_counts


def save_to_json(message, emoji_scores):
    """Extract relevant data from a message and store it in a dictionary format."""
    reactions_list = []
    reaction_counts = 0
    tags = get_tags(message.text)

    for reaction_count in message.reactions.results:
        emoticon = reaction_count.reaction.emoticon
        count = reaction_count.count
        reaction_counts += count
        reactions_list.append([emoticon, count])

    sum_values = sum([emoji[1] * emoji_scores.get(emoji[0], 1) for emoji in reactions_list])

    return {
        "pc_date": str(message.date.strftime("%d-%m-%Y %H:%M:%S")),
        "pc_text": message.text,
        "tags": tags,
        'tg_link': f"https://t.me/{tgID}/{message.id}",
        "emojis": {emoji[0]: round(emoji[1] * emoji_scores.get(emoji[0], 1), 2) for emoji in reactions_list},
        "total_reactions": reaction_counts,
        "sum": round(sum_values, 2)
    }


def write_to_file(data_list, norm_sum):
    """Save the processed data to a JSON file."""
    for idx, item in enumerate(data_list):
        item['norm_sum'] = norm_sum[idx]

    data_dict = {
        'tgID': tgID,
        'date': datetime.now().date().strftime("%d-%m-%Y"),
        'time': datetime.now().time().strftime("%H:%M:%S"),
        'norm_sum_min': min(norm_sum),
        'norm_sum_max': max(norm_sum),
        'data': sorted(data_list, key=lambda x: x['norm_sum']),
    }

    filename = f'data/parce_{tgID}_{datetime.today().strftime("%d%m%y%H%M")}.json'
    with open(filename, 'w') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


async def main():
    """Main asynchronous function to fetch and process telegram messages."""
    async with client:
        messages = await client.get_messages(f"@{tgID}", limit, add_offset=offset)

        with open("emoji_scores.json", "r") as file:
            emoji_scores = json.load(file)

        data_list = []
        for message in messages:
            if message.reactions:
                data_list.append(save_to_json(message, emoji_scores))
                time.sleep(.3)
        sum_array = [item["sum"] for item in data_list]

        norm_sum = standardize_array(sum_array)
        write_to_file(data_list, norm_sum)


with client:
    client.loop.run_until_complete(main())
