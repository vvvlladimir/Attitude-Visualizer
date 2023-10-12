import json
import time
from datetime import datetime

import openai
import tiktoken
from telethon import TelegramClient

from config import *

aiON = False
maxTokenLimit = 550
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


def getMainIdea(text):
    encoding = tiktoken.encoding_for_model(modelName)
    num_tokens = len(encoding.encode(text))
    print(num_tokens)
    if not aiON or num_tokens > maxTokenLimit:
        return text[:50]

    response = openai.Completion.create(
        engine=modelName,
        prompt=f"Summarize the following text in your own words in a very short sentence.:\n\n{text}",
        max_tokens=50
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


def saveToJson(summary, id, reactionsList, emojiScores, reactionCounts):
    tgLink = f"https://t.me/{tgID}/{id}"
    sum_values = 0
    emojiDict = {}
    for emoji in reactionsList:
        key = emoji[0]
        value = round(emoji[1] * emojiScores.get(emoji[0], None), 2)
        sum_values += value
        emojiDict[key] = value

    totalReactions.append(round(sum_values, 2))

    data = {
        "summary": summary,
        'tg_link': tgLink,
        "emojis": emojiDict,
        "total_reactions": reactionCounts,
        "sum": round(sum_values, 2)
    }

    dataList.append(data)


def writeToFile(norm_sum):
    currentDate = str(datetime.now().date().strftime("%d-%m-%Y"))
    currentTime = str(datetime.now().time().strftime("%H:%M:%S"))
    data_dict = {
        'date': currentDate,
        'time': currentTime,
        'data': dataList
    }

    key = 0
    for item in dataList:
        item['norm_sum'] = norm_sum[key]
        key += 1

    with open('parce_rbc.json', 'w') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


async def main():
    async with client:
        messages = await client.get_messages(f"@{tgID}", limit, add_offset=offset)

        for message in messages:
            reactionsList = []
            reactionCounts = 0
            summary = getMainIdea(message.text)

            for reaction_count in message.reactions.results:
                emoticon = reaction_count.reaction.emoticon
                count = reaction_count.count

                reactionCounts += count
                reactionsList.append([emoticon, count])

            saveToJson(summary, message.id, reactionsList, emojiScores, reactionCounts)
            time.sleep(1)

    norm_sum = normalizeTotalReactions(totalReactions)
    writeToFile(norm_sum)

with client:
   client.loop.run_until_complete(main())
