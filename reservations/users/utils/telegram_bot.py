import telepot

from user_profile.models import UserProfile
from django.db import IntegrityError

TOKEN = '606061796:AAFsveXNHQ75CssfRwJbxH1LrSo8HG5SX84'
bot = telepot.Bot(TOKEN)


def handle(msg):
    if 'entities' in msg and msg['entities'][0]['type'] == 'phone_number':
        try:
            profile = UserProfile.objects.get(telephone=msg['text'])
            profile.telegram_id = msg['chat']['id']
            try:
                profile.save()
            except IntegrityError:
                bot.sendMessage(msg['chat']['id'], 'This number already have Telegram.')
        except UserProfile.DoesNotExist:
            bot.sendMessage(msg['chat']['id'], 'Please enter valid phone number')
    elif msg['text'] == '/start':
        bot.sendMessage(msg['chat']['id'], 'Please enter your phone number. Format: +380xxxxxxxxx')


print('Listening...')




