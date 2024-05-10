from datetime import datetime
import pytz


def now_tehran():
    return datetime.now(tz=pytz.timezone('Iran'))


def datetime_difference_from_now(the_datetime: datetime):
    now_date = now_tehran()
    time_diff = int((the_datetime - now_date).total_seconds())
    return time_diff if time_diff > 0 else 0
