import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from pathlib import Path


load_dotenv()


cache_folder = Path(".cache")
sessions_folder = cache_folder / "sessions"
dates_folder = Path("dates")
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")


channelsIDs = []
channelsExtractedInfos = []
client: TelegramClient


async def addChannelsIDs():
    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            channelsIDs.append(dialog.id)


async def extractDates(channelsList):
    for channelID in channelsList:
        channel = await client.get_entity(channelID)
        joinedDate = channel.date.strftime("%B %d, %Y - %H:%M:%S")
        channelsExtractedInfos.append(f"{channel.title} : {joinedDate}")


def writeStrToFile(file, lines):
    filename = f"{file}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")
    print(f"Extracted dates saved to file: {filename}")


def getDateTimeNow():
    return datetime.today().strftime("%d %b, %Y - %H.%M")


def main():
    os.makedirs(cache_folder, exist_ok=True)
    os.makedirs(dates_folder, exist_ok=True)
    os.makedirs(sessions_folder, exist_ok=True)

    print("Please enter a session name:")
    sessionName = input()
    sessionLocation = sessions_folder / sessionName
    os.makedirs(sessionLocation, exist_ok=True)

    global client
    client = TelegramClient(sessionLocation / sessionName, api_id, api_hash)
    client.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(addChannelsIDs())
    loop.run_until_complete(extractDates(channelsIDs))
    writeStrToFile(dates_folder / getDateTimeNow(), channelsExtractedInfos)


if __name__ == "__main__":
    main()
