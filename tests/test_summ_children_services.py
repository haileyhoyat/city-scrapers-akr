from collections import defaultdict
from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import BOARD, COMMITTEE, TENTATIVE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.summ_children_services import SummChildrenServicesSpider

test_response = file_response(
    join(dirname(__file__), "files", "summ_children_services.html"),
    url=(
        "https://www.summitkids.org/Community-Action/Calendar/ModuleID/426/ItemID/1005/mctl/EventDetails"  # noqa
    ),
)
spider = SummChildrenServicesSpider()

freezer = freeze_time("2019-10-07")
freezer.start()

spider.link_date_map = defaultdict(list)
parsed_items = [item for item in spider._parse_detail(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 2


def test_title():
    assert parsed_items[0]["title"] == "Board of Trustees"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 10, 22, 17, 30)


def test_end():
    assert parsed_items[0]["end"] == datetime(2019, 10, 22, 18, 30)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "summ_children_services/201910221730/x/board_of_trustees"


def test_status():
    assert parsed_items[0]["status"] == TENTATIVE


def test_location():
    assert parsed_items[0]["location"] == spider.location


def test_source():
    assert parsed_items[0]["source"] == test_response.url


def test_links():
    assert parsed_items[0]["links"] == []


def test_classification():
    assert parsed_items[0]["classification"] == BOARD
    assert parsed_items[1]["classification"] == COMMITTEE


def test_all_day():
    assert parsed_items[0]["all_day"] is False
