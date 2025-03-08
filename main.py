from web_scraping import scrapers_repo
import json

from web_scraping.models.labeled_news import LabeledNews
from web_scraping.scrapers.scraper import Scraper


def main():
    # labeled_news = scrapers_repo.piaui_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.a_publica_scraper.collect_labeled_feed_entries()
    # labeled_news = scrapers_repo.a_publica_truco_scraper.collect_labeled_feed_entries()

    # labeled_news = scrapers_repo.checamos_scraper.collect_labeled_feed_entries()
    #

    scrapers: list[Scraper] = [
        scrapers_repo.aos_fatos_scraper,
        scrapers_repo.g1_scraper,
        scrapers_repo.e_farsas_scraper,
        scrapers_repo.boatos_scraper,
        scrapers_repo.g1_edu_scraper,
        scrapers_repo.g1_economia_scraper,
        scrapers_repo.g1_tech_scraper,
    ]

    for scraper in scrapers:
        labeled_news = scraper.collect_labeled_feed_entries()
        print("\n" + "=" * 80)
        print(f"\nScraper: {scraper.news_source.base_url}")
        print(f"\nNumber of labeled news: {len(labeled_news)}")

        if labeled_news:
            print("\nFirst labeled news:")
            print(json.dumps(labeled_news[0].to_dict(), indent=4))


if __name__ == "__main__":
    main()
