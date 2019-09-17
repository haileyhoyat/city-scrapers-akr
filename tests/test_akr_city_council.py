from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import CITY_COUNCIL, TENTATIVE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.akr_city_council import AkrCityCouncilSpider

test_response = file_response(
    join(dirname(__file__), "files", "akr_city_council.html"),
    url="http://www.akroncitycouncil.org/upcoming-meetings/",
)
test_detail_response = file_response(
    join(dirname(__file__), "files", "akr_city_council_detail.html"),
    url=(
        "https://onlinedocs.akronohio.gov/OnBaseAgendaOnline/Documents/ViewAgenda?meetingId=262&doctype=1"  # noqa
    ),
)

EXPECTED_LINKS = [{
    "title": "Agenda",
    "href":
        "https://onlinedocs.akronohio.gov/OnBaseAgendaOnline/Documents/ViewAgenda?meetingId=262&doctype=1"  # noqa
}]

spider = AkrCityCouncilSpider()

freezer = freeze_time("2019-09-16")
freezer.start()

parsed_filter_items = [item for item in spider.parse(test_response)]
parsed_items = [item for item in spider._parse_detail(test_detail_response, links=EXPECTED_LINKS)]

freezer.stop()


def test_count():
    assert len(parsed_filter_items) == 8
    assert len(parsed_items) == 4


def test_title():
    assert parsed_items[0]["title"] == "City Council"
    assert parsed_items[-1]["title"] == "Budget & Finance Committee"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 9, 16, 19, 0)
    assert parsed_items[-1]["start"] == datetime(2019, 9, 16, 15, 0)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "akr_city_council/201909161900/x/city_council"


def test_status():
    assert parsed_items[0]["status"] == TENTATIVE


def test_location():
    assert parsed_items[0]["location"] == spider.location


def test_source():
    assert parsed_items[0][
        "source"
    ] == "https://onlinedocs.akronohio.gov/OnBaseAgendaOnline/Documents/ViewAgenda?meetingId=262&doctype=1"  # noqa


def test_links():
    assert parsed_items[0]["links"] == EXPECTED_LINKS


def test_classification():
    assert parsed_items[0]["classification"] == CITY_COUNCIL


def test_all_day():
    assert parsed_items[0]["all_day"] is False
