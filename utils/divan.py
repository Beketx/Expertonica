# import requests
# from bs4 import BeautifulSoup
#
#
# def parse_ssr():
#     response = requests.get('https://anim-shop.ru/product-category/kostyumy/')
#     soup = BeautifulSoup(response.content, 'html.parser')
#     data = soup.select('div.woocommerce-loop-product__title h3')
#     print(data)
#     return data
#
# if __name__ == '__main__':
#     print('Anime rate:', parse_ssr())
import csv
import logging
import collections
import requests
import bs4

from main.models import ParseModel, HtmlPage

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('wb')

ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'brand_name',
        'url',
    ),
)

HEADERS = (
    'Бренд',
    'Ссылка'
)



class Client:

    def __init__(self):
        """
        Session повышает шанс что нас не заподозрят и не блокнут
        """
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36',
            'Accept-Language': 'ru',
        }

        self.result = []


    def load_page(self, page: int = None):
        """
        Грузим основную html страницу
        """
        url = 'https://divan24.kz/product-category/krovati/krovaty/'
        res = self.session.get(url=url)
        res.raise_for_status()
        HtmlPage.objects.create(text=res.text)
        return res.text

    def parse_page(self, text: str):
        """
        Выделяем нужный нам элемент и по ней пробегаемся
        """
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.w-grid-item-h')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):
        """
        По указанным нам элементам берем нужные нам данные. Такие как Название брэнда и Url товара
        """
        url_block = block.select_one('a')
        if not url_block:
            logger.error('noe url blcok')
            return

        url = url_block.get('href')
        if not url:
            logger.error('no href')
            return

        name_block = block.select_one('h3')
        if not name_block:
            logger.error(f'no name_block on {url}')
            return

        brand_name = name_block.select_one('a')
        if not brand_name:
            logger.error(f'no brand_name on {url}')
            return

        url = brand_name.get('href')
        if not url:
            logger.error('no href')
            return

        brand_name = brand_name.text
        ParseModel.objects.create(title=brand_name, url=url)

        logger.info('%s, %s', url, brand_name)

        self.result.append(ParseResult(
            url=url,
            brand_name=brand_name,
        ))
        logger.info('=' * 100)


    def save_result(self):
        """
        Дополнительно сохраняем их в csv файле
        """
        path = '/Users/beket/Desktop/parseme/test.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)


    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'Получили {len(self.result)} элементов')

        self.save_result()



"""
Running parser
"""
if __name__ == '__main__':
    parser = Client()
    parser.run()

