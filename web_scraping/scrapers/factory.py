from web_scraping.models.factory import NewsSourcesCollection, get_news_sources
from web_scraping.scrapers.scraper import (
    AosFatosScraper,
    G1Scraper,
    EFarsasScraper,
    BoatosScraper,
    G1EduScraper,
    G1EconomiaScraper,
    G1TechScraper,
)


class ScraperCollection:
    aos_fatos_scraper: AosFatosScraper
    g1_scraper: G1Scraper
    e_farsas_scraper: EFarsasScraper
    boatos_scraper: BoatosScraper
    g1_edu_scraper: G1EduScraper
    g1_economia_scraper: G1EconomiaScraper
    g1_tech_scraper: G1TechScraper

    def __init__(self, news_sources_collection: NewsSourcesCollection):
        self.aos_fatos_scraper = AosFatosScraper(news_sources_collection.aos_fatos)
        self.g1_scraper = G1Scraper(news_sources_collection.g1)
        self.e_farsas_scraper = EFarsasScraper(news_sources_collection.e_farsas)
        self.boatos_scraper = BoatosScraper(news_sources_collection.boatos)
        self.g1_edu_scraper = G1EduScraper(news_sources_collection.g1_edu)
        self.g1_economia_scraper = G1EconomiaScraper(
            news_sources_collection.g1_economia
        )
        self.g1_tech_scraper = G1TechScraper(news_sources_collection.g1_tech)


def get_scrapers():
    news_sources_collection = get_news_sources()
    return ScraperCollection(news_sources_collection)
