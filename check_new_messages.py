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


@client.on(events.NewMessage)
async def new_message(event):
    msg = event.message.message
    user_id = event.message.peer_id.user_id
    Log.info(f"{user_id}: {msg}")
    Log.info(event.stringify())


@client.on(events.MessageDeleted)
async def delete_message(event):
    msg = event.stringify()
    Log.info(msg)


@client.on(events.MessageEdited)
async def edit_message(event):
    msg = event.stringify()
    Log.info(msg)


# client.start()
# client.run_until_disconnected()
