from datetime import timedelta, timezone

# pip install python-decouple
from decouple import config

# pip install telethon
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import CheckChatInviteRequest
from telethon.tl.types import *

name = 'Patterns'
api_id = config('api_id', default='')
api_hash = config('api_hash', default='')
chat = 'huZKf6f_ggE5NTJi'

with TelegramClient(name, api_id, api_hash) as client:
    channel = client(CheckChatInviteRequest(chat)).chat
    for message in client.iter_messages(channel):
        if message.date < (datetime.now(timezone.utc) - timedelta(days=1)):
            break
        if message.reply_markup is not None or message.message.find('https://t.me/') > 0:
            continue

        date = message.date

        text = message.message
        for entity in reversed(message.entities):
            if isinstance(entity, MessageEntityBold):
                text = text[:(entity.offset + entity.length)] + '</b>' + text[(entity.offset + entity.length):]
                text = text[:entity.offset] + '<b>' + text[entity.offset:]
            elif isinstance(entity, MessageEntityItalic):
                text = text[:(entity.offset + entity.length)] + '</i>' + text[(entity.offset + entity.length):]
                text = text[:entity.offset] + '<i>' + text[entity.offset:]
        text = text.replace('\u200b', '')

        if message.media is not None:
            if isinstance(message.media, MessageMediaWebPage):
                url = message.media.webpage.url
            message.download_media(file="media/" + date.strftime('%Y.%m.%d %H-%M-%S') + '.jpg')

        f = open('articles/' + date.strftime('%Y.%m.%d %H-%M-%S') + '.txt', 'w', encoding='utf8')
        if 'url' in locals():
            f.writelines(text + '\n\n' + url)
        else:
            f.writelines(text)
        f.close()

        #print(message.stringify())
        #print("\n\n")
