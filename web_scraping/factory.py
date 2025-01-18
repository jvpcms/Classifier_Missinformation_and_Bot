from web_scraping.news_sources.factory import NewsSourcesCollection, get_news_sources
from web_scraping.scraper import (
    AosFatosScraper,
    PiauiScraper,
    G1Scraper,
    EFersasScraper,
    BoatosScraper,
    APublicaScraper,
    APublicaTrucoScraper,
    ChecamosScraper,
)


class ScraperCollection:
    aos_fatos_scraper: AosFatosScraper
    piaui_scraper: PiauiScraper
    g1_scraper: G1Scraper
    e_fersas_scraper: EFersasScraper
    boatos_scraper: BoatosScraper
    a_publica_scraper: APublicaScraper
    a_publica_truco_scraper: APublicaTrucoScraper
    checamos_scraper: ChecamosScraper

    def __init__(self, news_sources_collection: NewsSourcesCollection):
        self.aos_fatos_scraper = AosFatosScraper(news_sources_collection.aos_fatos)
        self.piaui_scraper = PiauiScraper(news_sources_collection.piaui)
        self.g1_scraper = G1Scraper(news_sources_collection.g1)
        self.e_fersas_scraper = EFersasScraper(news_sources_collection.e_farsas)
        self.boatos_scraper = BoatosScraper(news_sources_collection.boatos)
        self.a_publica_scraper = APublicaScraper(news_sources_collection.a_publica)
        self.a_publica_truco_scraper = APublicaTrucoScraper(
            news_sources_collection.a_publica_truco
        )
        self.checamos_scraper = ChecamosScraper(news_sources_collection.checamos)


def get_scrapers():
    news_sources_collection = get_news_sources()
    return ScraperCollection(news_sources_collection)
