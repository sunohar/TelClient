from telethon import TelegramClient, events
from util import Log, Log2
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


@Log.catch()
async def save_message(event, msgtype):
    peer_id = getattr(event.message.peer_id, "user_id", 0)
    from_id = getattr(event.message.from_id, "user_id", 0)
    alt_emoji = ""
    if from_id:
        sender = from_id
    else:
        sender = peer_id
    Log2.info(f"{ids.get(sender,sender)}: {event.message.message} (id:{event.message.id} {msgtype})")
    if peer_id in ids.keys():
        is_photo = getattr(event.message.media, "photo", 0)
        is_document = getattr(event.message.media, "document", 0)
        # if is_photo:
        #     ext = "png"
        # else:
        #     ext = "mp4"
        ext = "png"
        if is_document:
            mime_type = getattr(event.message.media.document, "mime_type", 0)
            if mime_type == "video/mp4":
                ext = "mp4"
            elif mime_type == "image/webp":
                ext = "webp"
            elif mime_type == "video/webm":
                ext = "webm"
            elif mime_type == "application/x-tgsticker":
                ext = "tgs"
                alt_emoji = event.message.media.document.attributes[1].alt
            else:
                ext = "gif"
        filename = f"./media/{event.message.id}.{ext}"

        Log.info(f"{ids[sender]}: {event.message.message + alt_emoji} (id:{event.message.id} {msgtype})")
        await client.download_media(event.message, filename)


@Log.catch()
@client.on(events.NewMessage)
async def new_message(event):
    try:
        Log.debug(event.stringify())
        await save_message(event, "new")

    except Exception as e:
        Log.error(e)


@Log.catch()
@client.on(events.MessageDeleted)
async def delete_message(event):
    try:
        Log.debug(event.stringify())
        base_del_class = type(event.original_update).__name__
        if base_del_class == "UpdateDeleteMessages":
            Log.info(f"deleted_ids: {event.deleted_ids}")
    except Exception as e:
        Log.error(e)


@Log.catch()
@client.on(events.MessageEdited)
async def edit_message(event):
    try:
        Log.debug(event.stringify())
        await save_message(event, "edited")
    except Exception as e:
        Log.error(e)


Log.info("Starting Telegram Client....")
Log.debug("If phone or bot token is asked then enter phone number including country code...")
client.start()
client.run_until_disconnected()
