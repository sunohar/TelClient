from telethon import TelegramClient, events
from util import Log
import yaml

# Read config
with open("config.yaml") as cfg:
    config = yaml.safe_load(cfg)

profile = config["profile"]

api_id = config[profile]["api_id"]
api_hash = config[profile]["api_hash"]
session = config[profile]["session"]
ids = config["ids"]
client = TelegramClient(session, api_id, api_hash)
Log.debug(f"{ids = }, {type(ids)}")


async def save_message(event, msgtype):
    peer_id = getattr(event.message.peer_id, "user_id", 0)
    from_id = getattr(event.message.from_id, "user_id", 0)
    if from_id:
        sender = from_id
    else:
        sender = peer_id
    if peer_id in ids.keys():
        Log.info(f"{ids[sender]}: {event.message.message} (id:{event.message.id} {msgtype})")
        filename = f"./media/{event.message.id}.png"
        await client.download_media(event.message, filename)


@client.on(events.NewMessage)
async def new_message(event):
    try:
        Log.debug(event.stringify())
        await save_message(event, "new")

    except Exception as e:
        Log.error(e)


@client.on(events.MessageDeleted)
async def delete_message(event):
    try:
        Log.debug(event.stringify())
        base_del_class = type(event.original_update).__name__
        if base_del_class == "UpdateDeleteMessages":
            Log.info(f"deleted_ids: {event.deleted_ids}")
    except Exception as e:
        Log.error(e)


@client.on(events.MessageEdited)
async def edit_message(event):
    try:
        Log.debug(event.stringify())
        await save_message(event, "edited")
    except Exception as e:
        Log.error(e)


Log.info("Starting Telegram Client....")
client.start()
client.run_until_disconnected()
