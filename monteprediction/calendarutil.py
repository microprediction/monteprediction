from datetime import datetime, timedelta


def get_last_wednesday():
    today = datetime.now()
    offset = (today.weekday() - 2) % 7
    last_wednesday = today - timedelta(days=offset)
    return last_wednesday.date()


def back_to_weekday(d):
    if d.weekday() == 5:  # Saturday
        end_date = d - timedelta(days=1)  # Previous day (Friday)
    elif d.weekday() == 6:  # Sunday
        end_date = d - timedelta(days=2)  # Two days before (Friday)
    else:
        end_date = d
    return end_date