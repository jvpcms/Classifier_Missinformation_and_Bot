from web_scraping.news_sources.news_sources import CheckingAgency, VirtualMedia


class NewsSourcesCollection:
    aos_fatos: CheckingAgency
    piaui: CheckingAgency
    g1: CheckingAgency
    e_farsas: CheckingAgency
    boatos: CheckingAgency
    a_publica: CheckingAgency
    a_publica_truco: CheckingAgency
    checamos: CheckingAgency
    g1_tech: VirtualMedia
    g1_edu: VirtualMedia
    g1_economia: VirtualMedia

    def __init__(self):
        self.aos_fatos = CheckingAgency(
            url="https://aosfatos.org/noticias/feed/",
        )

        self.piaui = CheckingAgency(
            url="https://piaui.folha.uol.com.br/feed/",
        )

        self.g1 = CheckingAgency(
            url="https://g1.globo.com/fato-ou-fake/",
        )

        self.e_farsas = CheckingAgency(
            url="https://www.e-farsas.com/feed",
        )

        self.boatos = CheckingAgency(
            url="https://www.boatos.org/feed",
        )

        self.a_publica = CheckingAgency(
            url="https://apublica.org/feed/",
        )

        self.a_publica_truco = CheckingAgency(
            url="https://apublica.org/feed/truco/",
        )

        self.checamos = CheckingAgency(
            url="https://checamos.afp.com/rss.xml",
        )

        self.g1_tech = VirtualMedia(
            url="https://g1.globo.com/rss/g1/tecnologia/",
        )

        self.g1_edu = VirtualMedia(
            url="https://g1.globo.com/rss/g1/educacao/",
        )

        self.g1_economia = VirtualMedia(
            url="https://g1.globo.com/rss/g1/economia/",
        )


def get_news_sources():
    return NewsSourcesCollection()
