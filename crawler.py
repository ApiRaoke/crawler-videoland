import string
import scrapy

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

        for contador_musicas in range(2, 42):

            CANTOR_SELECTOR = '//tr[{0:d}]/td[1]/font/text()'.format(contador_musicas)
            CODIGO_SELECTOR = '//tr[{0:d}]/td[2]/font/text()'.format(contador_musicas)
            TITULO_SELECTOR = '//tr[{0:d}]/td[3]/font/text()'.format(contador_musicas)
            LETRA_SELECTOR  = '//tr[{0:d}]/td[4]/font/text()'.format(contador_musicas)
            IDIOMA_SELECTOR = '//tr[{0:d}]/td[5]/font/text()'.format(contador_musicas)
            PACOTE_SELECTOR = '//tr[{0:d}]/td[6]/font/a/text()'.format(contador_musicas)

            # cantor: CANTOR
            # codigo: CÓD
            # titulo: TÍTULO
            # letra:  INÍCIO DA LETRA
            # idioma: IDIOMA
            # pacote: PACOTE

            yield {
                'total_pages': total_pages,
                'url':    response.url,
                'cantor': ''.join(response.xpath(CANTOR_SELECTOR).extract()),
                'codigo': ''.join(response.xpath(CODIGO_SELECTOR).extract()),
                'titulo': ''.join(response.xpath(TITULO_SELECTOR).extract()),
                'letra':  ''.join(response.xpath(LETRA_SELECTOR).extract()),
                'idioma': ''.join(response.xpath(IDIOMA_SELECTOR).extract()),
                'pacote': ''.join(response.xpath(PACOTE_SELECTOR).extract()),
            }

        total_mais_1 = total_pages + 1

        for contador_paginas in range(1, total_mais_1):
            url_current_page = response.url
            current_page_number = str(url_current_page.split('=')[-1])

            url_next_page = ''.join(url_current_page.rsplit(current_page_number,1)) + str(contador_paginas)

            # print(url_current_page, current_page_number, url_next_page)

            yield scrapy.Request(
                response.urljoin(url_next_page),
                callback=self.parse
            )



# em cada url (passando por todas as páginas)

    ## em cada página 
    
# trazer para o banco:

# cantor: CANTOR
# codigo: CÓD
# titulo: TÍTULO
# letra:  INÍCIO DA LETRA
# idioma: IDIOMA
# pacote: PACOTE


# Exemplo:
# https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=A&categoria=33&pagina=1
