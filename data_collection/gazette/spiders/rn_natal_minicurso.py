from datetime import datetime

# import pdb
import dateparser
from scrapy.http import FormRequest

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider

# roda sem baixar os arquivos:
# scrapy crawl rn_natal_minicurso -s FILES_STORE=""


class RnNatalSpider(BaseGazetteSpider):
    name = "rn_natal_minicurso"
    TERRITORY_ID = "2408102"
    start_urls = ["http://www.natal.rn.gov.br/dom/"]

    def parse(self, response):
        meses = [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
        ]  # months
        anos = range(2003, datetime.now().year + 1)  # years

        for ano in anos:

            for mes in meses:
                requisicao = FormRequest(
                    url="http://www.natal.rn.gov.br/dom/",
                    formdata={"mes": mes, "ano": str(ano)},
                    callback=self.parse_mes,
                )
                yield requisicao

    def parse_mes(self, response):
        gazettes = response.xpath('//a[contains(@href, ".pdf")]')
        for gazette in gazettes:
            link = gazette.xpath("./@href").get()
            texto = gazette.xpath("./text()").get()
            data = dateparser.parse(texto.split("-")[-1], languages=["pt"]).date()
            extra_edition = "Extra" in texto

            yield Gazette(
                date=data,
                file_urls=[link],
                is_extra_edition=extra_edition,
                power="executive_legislative",
            )


#        pdb.set_trace() #função compatível com breakpoint do python 3.8+
