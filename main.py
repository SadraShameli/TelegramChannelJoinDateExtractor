import os
import csv
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient
from pathlib import Path


load_dotenv()


CACHE_FOLDER = Path(".cache")
SESSIONS_FOLDER = CACHE_FOLDER / "sessions"
DATA_FOLDER = Path("data")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")


async def RetrieveData(session_folder):
    client = TelegramClient(session_folder, API_ID, API_HASH)
    await client.start()
    channels_id = []

    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            channels_id.append(dialog.id)

    file_date = DATA_FOLDER / datetime.today().strftime("%d %b, %Y - %H.%M")
    filename_txt = f"{file_date}.txt"
    filename_csv = f"{file_date}.csv"
    txt_content = []

    with open(filename_csv, "w", encoding="utf-8", newline="") as csv_file:
        fieldNames = ["Telegram Channel Name", "Channel Join Date", "Channel Link"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
        writer.writeheader()

        for channelId in channels_id:
            channel = await client.get_entity(channelId)

            channel_name = channel.title
            channel_joindate = channel.date.strftime("%B %d, %Y - %H:%M:%S")
            channel_link = (
                "https://t.me/" + channel.username if channel.username else " "
            )

            writer.writerow(
                {
                    fieldNames[0]: channel_name,
                    fieldNames[1]: channel_joindate,
                    fieldNames[2]: channel_link,
                }
            )
            txt_content.append(f"{channel_name}: {channel_joindate}")

    with open(filename_txt, "w", encoding="utf-8", newline="\n") as txt_file:
        txt_file.writelines(line + "\n" for line in txt_content)

    print(f"Extracted data saved to files: {filename_txt} and {filename_csv}")


def main():
    print("Please enter a session name:")
    session_name = "mozhgan"
    session_folder = SESSIONS_FOLDER / session_name

    os.makedirs(session_folder, exist_ok=True)
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)
    os.makedirs(SESSIONS_FOLDER, exist_ok=True)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(RetrieveData(session_folder / session_name))


if __name__ == "__main__":
    main()
