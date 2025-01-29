from web_scraping import scrapers_repo
import json

from web_scraping.models.labeled_news import LabeledNews
from web_scraping.scrapers.scraper import Scraper

# feedParser
# id
# url
# title
# date (published parsed)
# data rotulacao (created at)
# author
#
# source
# tipo (agencia / midia)
# url source
# pais

# Need
# rotulacao (fake, true)


def is_field_empty(field) -> bool:
    if field is None:
        return True
    if field == "":
        return True
    if field == []:
        return True
    if field == {}:
        return True
    if field == [""]:
        return True
    return False


def main():
    # labeled_news = scrapers_repo.checamos_scraper.collect_labeled_feed_entries()

    # labeled_news = scrapers_repo.aos_fatos_scraper.collect_labeled_feed_entries()
    labeled_news = scrapers_repo.g1_scraper.collect_labeled_feed_entries()

    # labeled_news = scrapers_repo.piaui_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.e_farsas_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.boatos_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.a_publica_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.a_publica_truco_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.g1_edu_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.g1_economia_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.g1_tech_scraper.collect_labeled_feed_entries()


if __name__ == "__main__":
    main()
