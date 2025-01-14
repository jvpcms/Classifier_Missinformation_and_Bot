from web_scraping import (
    aos_fatos_scraper,
    piaui_scraper,
    g1_scraper,
    e_fersas_scraper,
    boatos_scraper,
    a_publica_scraper,
    a_publica_truco_scraper,
    checamos_scraper,
)
from reddit_api import postInterface
from web_scraping.scraper import Scraper


def main():
    scrapers = [
        aos_fatos_scraper,
        piaui_scraper,
        g1_scraper,
        e_fersas_scraper,
        boatos_scraper,
        a_publica_scraper,
        a_publica_truco_scraper,
    ]

    for scraper in scrapers:
        entries = scraper.get_feed_entries()
        print(entries[0])


if __name__ == "__main__":
    main()
