import string
import scrapy
import hashlib

class VideolandCrawler(scrapy.Spider):

    name = "videoland_crawler"

    urls_alfabetic = ['https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=%s&categoria=33&pagina=1' %(letter) for letter in list(string.ascii_uppercase)]
    urls_numeric = ['https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=%s&categoria=33&pagina=1' %(number) for number in range(0, 10)]

    start_urls = urls_alfabetic + urls_numeric

    # print(start_urls)

    def parse(self, response):
        PAGINA_SELECTOR = '//b[contains(., "Página ")]/text()'
        total_pages = int(response.xpath(
            PAGINA_SELECTOR).extract_first().split()[-1])
        # print(total_pages)

        yield scrapy.Request(
            response.url,
            callback=self.parse_page,
            meta={'total_pages': total_pages}
        )

        for contador_paginas in range(1, total_pages + 1):
            url_current_page = response.url
            current_page_number = str(url_current_page.split('=')[-1])

            url_next_page = ''.join(
                url_current_page.rsplit(
                    current_page_number, 1)
                ) + str(contador_paginas)

            yield scrapy.Request(
                response.urljoin(url_next_page),
                callback=self.parse_page,
                meta={'total_pages': total_pages}
            )

    def parse_page(self, response):
        for contador_musicas in range(2, 42):

            CANTOR_SELECTOR = '//tr[{0:d}]/td[1]/font/text()'.format(contador_musicas)
            CODIGO_SELECTOR = '//tr[{0:d}]/td[2]/font/text()'.format(contador_musicas)
            TITULO_SELECTOR = '//tr[{0:d}]/td[3]/font/text()'.format(contador_musicas)
            LETRA_SELECTOR = '//tr[{0:d}]/td[4]/font/text()'.format(contador_musicas)
            IDIOMA_SELECTOR = '//tr[{0:d}]/td[5]/font/text()'.format(contador_musicas)
            PACOTE_SELECTOR = '//tr[{0:d}]/td[6]/font/a/text()'.format(contador_musicas)

            url = response.url

            total_pages = response.meta.get('total_pages')
            current_page = url.split('=')[-1]
            
            current_artist_search = url.split('=')[-3].split('&')[0]

            music_page_order = contador_musicas - 1

            cantor = response.xpath(CANTOR_SELECTOR).extract_first()
            codigo = response.xpath(CODIGO_SELECTOR).extract_first()
            titulo = response.xpath(TITULO_SELECTOR).extract_first()
            letra =  response.xpath(LETRA_SELECTOR).extract_first()
            idioma = response.xpath(IDIOMA_SELECTOR).extract_first()
            pacote = response.xpath(PACOTE_SELECTOR).extract_first()

            # cantor: CANTOR
            # codigo: CÓD
            # titulo: TÍTULO
            # letra:  INÍCIO DA LETRA
            # idioma: IDIOMA
            # pacote: PACOTE

            yield {
                'md5': hashlib.md5(
                    (
                        url + str(total_pages) + cantor + codigo +
                        titulo + letra + idioma + pacote
                    ).encode('utf-8')
                ).hexdigest(),
                'url': url,
                'total_pages': total_pages,
                'current_page': current_page,
                'music_page_order': music_page_order,
                'current_artist_search': current_artist_search,
                'cantor': cantor,
                'codigo': codigo,
                'titulo': titulo,
                'letra': letra,
                'idioma': idioma,
                'pacote': pacote,
            }
