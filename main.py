from web_scraping import scrapers


def main():
    scrapers_checking_agency_list = [
        scrapers.a_publica_scraper,
        scrapers.a_publica_truco_scraper,
        scrapers.aos_fatos_scraper,
        scrapers.boatos_scraper,
        scrapers.e_farsas_scraper,
        scrapers.g1_scraper,
        scrapers.piaui_scraper,
        scrapers.checamos_scraper,
    ]
    scrapers_virtual_media_list = [
        scrapers.g1_tech_scraper,
        scrapers.g1_edu_scraper,
        scrapers.g1_economia_scraper,
    ]

    for scraper in scrapers_virtual_media_list:
        print("=====================================")
        print(scraper.__class__.__name__)
        scraper.get_feed_entries()


if __name__ == "__main__":
    main()
