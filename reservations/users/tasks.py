from reservations.celery import app
from .utils.telegram_bot import bot

@app.task
def send_notification(telegram_id, restaurant):
    bot.sendMessage(
        telegram_id,
        'Notification: You have reserve table in an hour. Restaurant:' + restaurant
    )
