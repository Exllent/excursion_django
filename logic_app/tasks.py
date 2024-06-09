from celery import shared_task
from ex_site import settings
import requests
from time import sleep


@shared_task()
def send_message_in_chat_tg(text: str):
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{settings.TELEGRAMM_TOKEN}/sendMessage?chat_id={settings.GROUP_ID}&text={text}")
        if response.status_code != 200:
            raise Exception
    except Exception:
        sleep(3)
        requests.get(
            f"https://api.telegram.org/bot{settings.TELEGRAMM_TOKEN}/sendMessage?chat_id={settings.GROUP_ID}&text={text}")
    except:
        pass
