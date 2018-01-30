import string
import scrapy


class VideolandCrawler(scrapy.Spider):
    name = "videoland_crawler"
    # url1 = "https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=A&categoria=33&pagina=1"

    urls_alfabetic = ['https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=%s&categoria=33&pagina=1' %(letter) for letter in list(string.ascii_uppercase)]
    urls_numeric = ['https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=%s&categoria=33&pagina=1' %(number) for number in range(0, 10)]

    start_urls = urls_alfabetic + urls_numeric

    print(start_urls)

    def parse(self, response):
        PAGINA_SELECTOR = '//b[contains(., "Página ")]'
        total_pages = response.xpath(PAGINA_SELECTOR).extract_first().replace('<b>', '').replace('</b>', '').split()[-1]
        print(total_pages)

# # de 0-9

# # de A-Z

# # buscar todas as urls       
    
# trazer para o banco:

# cantor: CANTOR
# codigo: CÓD
# titulo: TÍTULO
# letra:  INÍCIO DA LETRA
# idioma: IDIOMA
# pacote: PACOTE


# Exemplo:
# https://www.videoland.com.br/wwwroot/pesquisa.asp?artista=A&categoria=33&pagina=1
