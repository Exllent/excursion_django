from datetime import datetime, timedelta
from pytz import timezone


def current_datetime_msk():
    current_time_msk = datetime.now(timezone('Europe/Moscow'))
    return current_time_msk.strftime('%Y-%m-%d %H:%M')


def current_date_msk():
    current_datetime_utc = datetime.utcnow()
    current_date_time_msk = timezone('Europe/Moscow').localize(current_datetime_utc)
    return current_date_time_msk.date()


def current_date_msk_with_timedelta(days: int):
    return current_date_msk() + timedelta(days=days)
