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
        a_publica_scraper,
        a_publica_truco_scraper,
        aos_fatos_scraper,
        boatos_scraper,
        e_fersas_scraper,
        g1_scraper,
        piaui_scraper,
    ]

    # for scraper in scrapers:
    scraper = piaui_scraper
    print("=====================================")
    print(scraper.__class__.__name__)
    scraper.collect_data()


if __name__ == "__main__":
    main()
