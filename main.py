from web_scraping import scrapers


def main():
    scrapers_list = [
        scrapers.a_publica_scraper,
        scrapers.a_publica_truco_scraper,
        scrapers.aos_fatos_scraper,
        scrapers.boatos_scraper,
        scrapers.e_farsas_scraper,
        scrapers.g1_scraper,
        scrapers.piaui_scraper,
        scrapers.checamos_scraper,
    ]

    for scraper in scrapers_list:
        print("=====================================")
        print(scraper.__class__.__name__)
        scraper.collect_data()


if __name__ == "__main__":
    main()
