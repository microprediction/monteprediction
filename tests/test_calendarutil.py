from monteprediction.calendarutil import get_last_wednesday, back_to_weekday
import pytest
from datetime import datetime, timedelta, date


def test_get_last_wednesday_day():
    assert get_last_wednesday().weekday() == 2  # 2 represents Wednesday


def test_get_last_wednesday_not_future():
    assert get_last_wednesday() <= datetime.now().date()


def test_back_to_weekday_type():
    assert isinstance(get_last_wednesday(), date)


def test_back_to_weekday_weekday():
    for day in range(0, 5):  # Monday to Friday
        random_day = datetime.now().date() - timedelta(days=(datetime.now().weekday() - day))
        assert back_to_weekday(random_day) == random_day


def test_back_to_weekday_saturday():
    saturday = datetime.now().date() + timedelta(days=(5 - datetime.now().weekday()))
    assert back_to_weekday(saturday) == saturday - timedelta(days=1)


def test_back_to_weekday_sunday():
    sunday = datetime.now().date() + timedelta(days=(6 - datetime.now().weekday()))
    assert back_to_weekday(sunday) == sunday - timedelta(days=2)



if __name__ == "__main__":
    pytest.main(["-v"])
