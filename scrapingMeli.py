import requests
from bs4 import BeautifulSoup
from lxml import etree

def productos(producto):
    siguiente = 'https://listado.mercadolibre.com.ar/'+producto
    lista_titulos = []
    lista_urls = []
    lista_precios = []
    while True:
        r = requests.get(siguiente)
        if r.status_code == 200:
            #Titulos
            soup = BeautifulSoup(r.content,'html.parser')
            titulos = soup.find_all('h2',attrs={"class":"ui-search-item__title"})
            titulos = [i.text for i in titulos]
            lista_titulos.extend(titulos)
            #Urls
            urls = soup.find_all('a',attrs={"class":"ui-search-item__group__element ui-search-link"})
            urls = [i.get('href') for i in urls]
            lista_urls.extend(urls)
            #Precios
            dom = etree.HTML(str(soup))
            precios = dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__content-columns"]/div[@class="ui-search-result__content-column ui-search-result__content-column--left"]/div[1]/div//div[@class="ui-search-price__second-line"]//span[@class="andes-money-amount__fraction"]')
            precios = [i.text for i in precios]
            lista_precios.extend(precios)

            cantidad = soup.find('li',attrs={"class":"andes-pagination__page-count"})
            cantidad = int(cantidad.text.split(" ")[1])

            inicial = soup.find('span',attrs={"class":"andes-pagination__link"})
            inicial = int(inicial.text)
        else:
            break
        print(inicial,cantidad)
        if inicial == cantidad:
            break
        siguiente = dom.xpath('//li[@class="andes-pagination__button andes-pagination__button--next"]/a')[0].get('href')

    return lista_titulos, lista_urls, lista_precios