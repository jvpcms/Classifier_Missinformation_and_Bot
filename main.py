from datetime import datetime, timedelta
from web_scraping import scrapers_repo

from web_scraping.models.labeled_news import LabeledNews
from web_scraping.scrapers.scraper import Scraper

# from database import repos
#
# labeled_news_repo = repos.labeled_news
# news_sources_repo = repos.news_sources

DATE_FILTER = datetime.now() - timedelta(days=1)


def main():
    scrapers: list[Scraper] = [
        scrapers_repo.aos_fatos_scraper,
        scrapers_repo.g1_scraper,
        scrapers_repo.e_farsas_scraper,
        scrapers_repo.boatos_scraper,
        scrapers_repo.g1_edu_scraper,
        scrapers_repo.g1_economia_scraper,
        scrapers_repo.g1_tech_scraper,
    ]

    labeled_news: list[LabeledNews] = []

    for scraper in scrapers:
        labeled_news = labeled_news + scraper.collect_labeled_feed_entries(DATE_FILTER)


if __name__ == "__main__":
    print(DATE_FILTER)
    main()
