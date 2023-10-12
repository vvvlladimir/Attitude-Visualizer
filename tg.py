import json
import time
from datetime import datetime

import openai
from telethon import TelegramClient

from config import *

AI = False
limit = 5
offset = 30
tgID = "rbc_news"
modelName = 'text-davinci-002'

client = TelegramClient('tg_parcer', api_id, api_hash)
openai.api_key = api_key
dataList = []
totalReactions = []

with open("emoji_scores.json", "r") as file:
    emojiScores = json.load(file)


def getTags(text):
    if not AI:
        return "-"

    response = openai.Completion.create(
        engine=modelName,
        prompt=f"print one hashtag that describes the text as accurately as possible:\n\n{text}",
        max_tokens=5
    )

    return response.choices[0].text.strip()


def normalizeTotalReactions(totalReactions):
    min_count = min(totalReactions)
    max_count = max(totalReactions)

    if min_count == max_count:
        return totalReactions

    normalized_counts = []
    for x in totalReactions:
        normalized_x = (x - min_count) / (max_count - min_count)
        normalized_counts.append(normalized_x)

    return normalized_counts


def saveToJson(text, tags, id, reactionsList, emojiScores, reactionCounts, date):
    tgLink = f"https://t.me/{tgID}/{id}"
    sum_values = 0
    emojiDict = {}
    for emoji in reactionsList:
        key = emoji[0]
        if emoji[0] not in emojiScores:
            value = emoji[1]
        else: value = round(emoji[1] * emojiScores.get(emoji[0], None), 2)
        sum_values += value
        emojiDict[key] = value

    totalReactions.append(round(sum_values, 2))

    data = {
        "pc_date": str(date.strftime("%d-%m-%Y %H:%M:%S")),
        "pc_text": text,
        "tags": tags,
        'tg_link': tgLink,
        "emojis": emojiDict,
        "total_reactions": reactionCounts,
        "sum": round(sum_values, 2)
    }

    dataList.append(data)


def writeToFile(norm_sum):
    key = 0
    for item in dataList:
        item['norm_sum'] = norm_sum[key]
        key += 1

    sortList = sorted(dataList, key=lambda x: x['norm_sum'])

    currentDate = str(datetime.now().date().strftime("%d-%m-%Y"))
    currentTime = str(datetime.now().time().strftime("%H:%M:%S"))
    data_dict = {
        'tgID': tgID,
        'date': currentDate,
        'time': currentTime,
        'data': sortList
    }

    with open(f'data/parce_{tgID}.json', 'w') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


async def main():
    async with client:
        messages = await client.get_messages(f"@{tgID}", limit, add_offset=offset)

        for message in messages:
            reactionsList = []
            reactionCounts = 0
            tags = getTags(message.text)

            for reaction_count in message.reactions.results:
                emoticon = reaction_count.reaction.emoticon
                count = reaction_count.count

                reactionCounts += count
                reactionsList.append([emoticon, count])

            saveToJson(message.text, tags, message.id, reactionsList, emojiScores, reactionCounts, message.date)
            time.sleep(.3)

    norm_sum = normalizeTotalReactions(totalReactions)
    writeToFile(norm_sum)


with client:
    client.loop.run_until_complete(main())
