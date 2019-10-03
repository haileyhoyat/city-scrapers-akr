from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import BOARD, PASSED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.summ_board_health import SummBoardHealthSpider

test_response = file_response(
    join(dirname(__file__), "files", "summ_board_health.html"),
    url="https://www.scph.org/board-health",
)
spider = SummBoardHealthSpider()

freezer = freeze_time("2019-10-03")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_count():
    assert len(parsed_items) == 9


def test_title():
    assert parsed_items[0]["title"] == "Board of Health"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2019, 1, 10, 17, 0)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "summ_board_health/201901101700/x/board_of_health"


def test_status():
    assert parsed_items[0]["status"] == PASSED


def test_location():
    assert parsed_items[0]["location"] == spider.location


def test_source():
    assert parsed_items[0]["source"] == test_response.url


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href":
                "https://www.scph.org/sites/default/files/editor/BOHagendas/1%2010%2019%20PUBLIC%20AGENDA.pdf",  # noqa
            "title": "Agenda"
        },
        {
            "title": "Minutes",
            "href":
                "https://www.scph.org/sites/default/files/editor/BOHminutes/January%2010%202019%20Board%20Meeting%20Minutes%20with%20Schedules.pdf"  # noqa
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


def test_all_day():
    assert parsed_items[0]["all_day"] is False
