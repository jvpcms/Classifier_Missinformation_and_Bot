from web_scraping.models.news_sources import NewsSource


class NewsSourcesCollection:
    aos_fatos: NewsSource
    piaui: NewsSource
    g1: NewsSource
    e_farsas: NewsSource
    boatos: NewsSource
    a_publica: NewsSource
    a_publica_truco: NewsSource
    checamos: NewsSource
    g1_tech: NewsSource
    g1_edu: NewsSource
    g1_economia: NewsSource

    def __init__(self):
        self.aos_fatos = NewsSource(
            feed_url="https://aosfatos.org/noticias/feed/",
            base_url="https://aosfatos.org/",
            country="br",
            source_type="checking_agency",
        )

        self.piaui = NewsSource(
            feed_url="https://piaui.folha.uol.com.br/lupa/feed/",
            base_url="https://piaui.folha.uol.com.br/",
            country="br",
            source_type="checking_agency",
        )

        self.g1 = NewsSource(
            feed_url="https://g1.globo.com/rss/g1/fato-ou-fake/",
            base_url="https://g1.globo.com/fato-ou-fake/",
            country="br",
            source_type="checking_agency",
        )

        self.e_farsas = NewsSource(
            feed_url="https://www.e-farsas.com/feed",
            base_url="https://www.e-farsas.com/",
            country="br",
            source_type="checking_agency",
            feed_url_true_news="https://www.e-farsas.com/secoes/verdadeiro-2/feed",
            feed_url_fake_news="https://www.e-farsas.com/secoes/falso-2/feed",
        )

        self.boatos = NewsSource(
            feed_url="https://www.boatos.org/feed",
            base_url="https://www.boatos.org/",
            country="br",
            source_type="checking_agency",
        )

        self.a_publica = NewsSource(
            feed_url="https://apublica.org/feed/",
            base_url="https://apublica.org/",
            country="br",
            source_type="checking_agency",
        )

        self.a_publica_truco = NewsSource(
            feed_url="https://apublica.org/tag/truco/feed/",
            base_url="https://apublica.org/tag/truco/",
            country="br",
            source_type="checking_agency",
        )

        self.checamos = NewsSource(
            feed_url="https://checamos.afp.com/",
            base_url="https://checamos.afp.com/",
            country="br",
            source_type="checking_agency",
        )

        self.g1_tech = NewsSource(
            feed_url="https://g1.globo.com/rss/g1/tecnologia/",
            base_url="https://g1.globo.com/tecnologia/",
            country="br",
            source_type="virtual_media",
        )

        self.g1_edu = NewsSource(
            feed_url="https://g1.globo.com/rss/g1/educacao/",
            base_url="https://g1.globo.com/educacao/",
            country="br",
            source_type="virtual_media",
        )

        self.g1_economia = NewsSource(
            feed_url="https://g1.globo.com/rss/g1/economia/",
            base_url="https://g1.globo.com/economia/",
            country="br",
            source_type="virtual_media",
        )


def get_news_sources():
    return NewsSourcesCollection()
