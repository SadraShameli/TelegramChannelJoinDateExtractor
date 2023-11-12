import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

cache_folder = os.getenv("CACHE_FOLDER")
sessions_folder = os.getenv("SESSIONS_FOLDER")
data_folder = os.getenv("DATA_FOLDER")
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

channelsIDs = []
channelsExtractedInfos = []
client = None


async def addChannelsIDs():
    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            channelsIDs.append(dialog.id)


async def addChannelsExtractedData(channelsList):
    for channelID in channelsList:
        channel = await client.get_entity(channelID)
        joinedDate = channel.date.strftime("%B %d, %Y - %H:%M:%S")
        channelsExtractedInfos.append(f"{channel.title} : {joinedDate}")


def writeStrToFile(filename, lines):
    filenameWithExtention = f"{filename}.txt"
    with open(filenameWithExtention, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(f"{line}\n")
    print(f"Extracted data saved to file: {filenameWithExtention}")


def getDateTimeNow():
    return datetime.today().strftime("%d_%m_%Y - %H_%M_%S")


def main():
    print("Please enter a session name:")

    sessionName = input()
    sessionsFolder = f"{sessions_folder}/{sessionName}"

    global client
    client = TelegramClient(sessionsFolder, api_id, api_hash)
    client.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(addChannelsIDs())
    loop.run_until_complete(addChannelsExtractedData(channelsIDs))
    writeStrToFile(f"{data_folder}/{getDateTimeNow()}", channelsExtractedInfos)


if __name__ == "__main__":
    main()
