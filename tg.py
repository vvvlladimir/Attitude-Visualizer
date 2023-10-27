import json
import time
from datetime import datetime

# import openai
from telethon import TelegramClient


# AI = False
# modelName = 'text-davinci-002'

# post_limit = 0
# post_offset = 0
# channel_link = ""
# telegram_id = 0
# telegram_hash = ''


# openai.api_key = api_key


# def get_tags(text):
#     """Retrieve tags for a given text using OpenAI API."""
#     if not AI:
#         return "-"
#
#     response = openai.Completion.create(
#         engine=modelName,
#         prompt=f"print one hashtag that describes the text as accurately as possible:\n\n{text}",
#         max_tokens=5
#     )
#     return response.choices[0].text.strip()


def normalize_array(sum_array):
    """Normalize the total reactions to a range between 0 and 1."""
    min_count = min(sum_array)
    max_count = max(sum_array)

    if min_count == max_count:
        return sum_array

    normalized_counts = []
    for x in sum_array:
        normalized_x = 1 + ((x - min_count) / (max_count - min_count))
        normalized_counts.append(normalized_x)

    return normalized_counts


def standardize_array(sum_array):
    if len(sum_array) == 0:
        sum_array.append(0)
        return sum_array

    mean_value = sum(sum_array) / len(sum_array)
    std_dev = (sum([(x - mean_value) ** 2 for x in sum_array]) / len(sum_array)) ** 0.5

    # If standard deviation is zero, return the original array to avoid division by zero
    if std_dev == 0:
        return sum_array

    standardized_counts = [(x - mean_value) / std_dev for x in sum_array]

    return standardized_counts


def save_to_json(message, emoji_scores, channel_link):
    """Extract relevant data from a message and store it in a dictionary format."""
    reactions_list = []
    reaction_counts = 0
    # tags = get_tags(message.text)

    for reaction_count in message.reactions.results:
        emoticon = reaction_count.reaction.emoticon
        count = reaction_count.count
        reaction_counts += count
        reactions_list.append([emoticon, count])

    sum_values = sum([emoji[1] * emoji_scores.get(emoji[0], 1) for emoji in reactions_list])

    return {
        "pc_date": str(message.date.strftime("%d.%m.%Y %H:%M")),
        "pc_text": message.text,
        # "tags": tags,
        'tg_link': f"https://t.me/{channel_link}/{message.id}",
        "emojis": {emoji[0]: round(emoji[1] * emoji_scores.get(emoji[0], 1), 2) for emoji in reactions_list},
        "total_reactions": reaction_counts,
        "sum": round(sum_values, 2)
    }


def write_to_file(data_list, norm_sum, norm_views, channel_link, post_limit):
    """Save the processed data to a JSON file."""
    for idx, item in enumerate(data_list):
        item['norm_sum'] = norm_sum[idx]
        item['norm_views'] = norm_views[idx]

    data_dict = {
        'tgID': channel_link,
        'date': datetime.now().date().strftime("%d.%m.%Y"),
        'time': datetime.now().time().strftime("%H:%M"),
        'norm_sum_min': min(norm_sum),
        'norm_sum_max': max(norm_sum),
        'data': sorted(data_list, key=lambda x: x['norm_sum']),
    }

    filename = f'data/{channel_link}_{datetime.today().strftime("%H-%M_%d-%m-%Y")}_{post_limit}.json'
    with open(filename, 'w', encoding="utf-8") as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


async def main():
    try:
        with open("config.json", "r") as file:
            data = json.load(file)

        telegram_id = data.get("telegram_id", "")
        telegram_hash = data.get("telegram_hash", "")
        post_limit = data.get("post_limit", "")
        post_offset = data.get("post_offset", "")
        channel_link = data.get("channel_link", "")

    except FileNotFoundError:
        telegram_id = ""
        telegram_hash = ""
        post_limit = ""
        post_offset = ""
        channel_link = ""

    if channel_link.startswith("@"):
        channel_link = channel_link[1:]

    client = TelegramClient('client', telegram_id, telegram_hash)

    """Main asynchronous function to fetch and process telegram messages."""
    async with client:
        try:
            messages = await client.get_messages(f"@{channel_link}", post_limit, add_offset=post_offset)

            with open("emoji_scores.json", "r") as file:
                emoji_scores = json.load(file)

            data_list = []
            views_list = []
            for message in messages:
                if message.reactions:
                    data_list.append(save_to_json(message, emoji_scores, channel_link))
                    views_list.append(message.views)
                    time.sleep(.3)
            sum_array = [item["sum"] for item in data_list]

            norm_sum = standardize_array(sum_array)
            norm_views = normalize_array(views_list)
            write_to_file(data_list, norm_sum, norm_views, channel_link, post_limit)
        except:
            return
