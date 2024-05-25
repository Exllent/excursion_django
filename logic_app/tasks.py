from celery import shared_task
from ex_site import settings
import requests


@shared_task()
def send_message_in_chat_tg(text: str):
    requests.get(f"https://api.telegram.org/bot{settings.TELEGRAMM_TOKEN}/sendMessage?chat_id={settings.GROUP_ID}&text={text}")
