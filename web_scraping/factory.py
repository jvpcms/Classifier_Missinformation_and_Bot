from web_scraping.scraper import AosFatosScraper


class ScraperCollection:
    aos_fatos_scraper: AosFatosScraper

    def __init__(self):
        self.aos_fatos_scraper = AosFatosScraper()


def get_scrapers():
    return ScraperCollection()
