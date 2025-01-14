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
    piuai_scraper: PiauiScraper
    g1_scraper: G1Scraper
    e_fersas_scraper: EFersasScraper
    boatos_scraper: BoatosScraper
    a_publica_scraper: APublicaScraper
    a_publica_truco_scraper: APublicaTrucoScraper
    checamos_scraper: ChecamosScraper

    def __init__(self):
        self.aos_fatos_scraper = AosFatosScraper()
        self.piuai_scraper = PiauiScraper()
        self.g1_scraper = G1Scraper()
        self.e_fersas_scraper = EFersasScraper()
        self.boatos_scraper = BoatosScraper()
        self.a_publica_scraper = APublicaScraper()
        self.a_publica_truco_scraper = APublicaTrucoScraper()
        self.checamos_scraper = ChecamosScraper()


def get_scrapers():
    return ScraperCollection()
