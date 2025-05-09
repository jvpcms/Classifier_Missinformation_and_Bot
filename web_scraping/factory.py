from typing import List, Union
from models.news_sources import NewsSourcesCollection, get_news_sources
from web_scraping.scraper import (
    AosFatosScraper,
    G1Scraper,
    EFarsasScraper,
    BoatosScraper,
    G1EduScraper,
    G1EconomiaScraper,
    G1TechScraper,
)

from custom_logging.custom_logger import get_logger


class ScraperCollection:
    aos_fatos_scraper: AosFatosScraper
    g1_scraper: G1Scraper
    e_farsas_scraper: EFarsasScraper
    boatos_scraper: BoatosScraper
    g1_edu_scraper: G1EduScraper
    g1_economia_scraper: G1EconomiaScraper
    g1_tech_scraper: G1TechScraper

    def __init__(self, news_sources_collection: NewsSourcesCollection):
        self.aos_fatos_scraper = AosFatosScraper(
            news_sources_collection.aos_fatos,
            get_logger("aos_fatos_scraper"),
        )
        self.g1_scraper = G1Scraper(
            news_sources_collection.g1, get_logger("g1_scraper")
        )
        self.e_farsas_scraper = EFarsasScraper(
            news_sources_collection.e_farsas, get_logger("e_farsas_scraper")
        )
        self.boatos_scraper = BoatosScraper(
            news_sources_collection.boatos, get_logger("boatos_scraper")
        )
        self.g1_edu_scraper = G1EduScraper(
            news_sources_collection.g1_edu, get_logger("g1_edu_scraper")
        )
        self.g1_economia_scraper = G1EconomiaScraper(
            news_sources_collection.g1_economia,
            get_logger("g1_economia_scraper"),
        )
        self.g1_tech_scraper = G1TechScraper(
            news_sources_collection.g1_tech, get_logger("g1_tech_scraper")
        )

    def get_scrapers(
        self,
    ) -> List[
        Union[
            AosFatosScraper,
            G1Scraper,
            EFarsasScraper,
            BoatosScraper,
            G1EduScraper,
            G1EconomiaScraper,
            G1TechScraper,
        ]
    ]:
        """Return a list of all scrapers"""

        return [
            self.aos_fatos_scraper,
            self.g1_scraper,
            self.e_farsas_scraper,
            self.boatos_scraper,
            self.g1_edu_scraper,
            self.g1_economia_scraper,
            self.g1_tech_scraper,
        ]


def get_scraper_collection():
    news_sources_collection = get_news_sources()
    return ScraperCollection(news_sources_collection)
