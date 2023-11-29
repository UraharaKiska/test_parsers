from bs4 import BeautifulSoup
import lxml
import requests
from fake_useragent import UserAgent
import json


datas = []


def get_product_href(url, pages):
    url_main = "https://online.metro-cc.ru"
    with requests.Session() as session:
        for p in range(1, pages+1):
            useragent = UserAgent()
            headers = {
            "accept": "*/*",
            "user-agent": f"{useragent.random}",     
                }

            with session.get(url+str(p), headers=headers) as resp:
                # print(resp.status)
                if resp.status_code == 200:
                    print(f"Получена {p}-я страница")
                    soup = BeautifulSoup(resp.text, "lxml")
                    try:
                        inner = soup.find("div", id="products-inner")
                        data = inner.find_all("div", class_="product-card__content")
                        for d in data:
                            info = {}
                            try:
                                photo = d.find("div", class_="product-card-photo__content")
                                link = photo.find_next()['href']
                                info['url'] = url_main + link
                            except Exception as ex:
                                info['url'] = None
                            try:
                                price_block = d.find("div", class_="product-unit-prices__actual-wrapper")
                                new_price = price_block.find("span", class_="product-price__sum-rubles").text
                                info['new_price'] = new_price
                            except Exception as es:
                                info['new_price'] = None
                            try:
                                price_block = d.find("div", class_="product-unit-prices__old-wrapper")
                                old_price = price_block.find("span", class_="product-price__sum-rubles").text
                                info['old_price'] = old_price
                            except Exception as ex:
                                info['old_price'] = None
                            try:
                                name = soup.find("span", class_="product-card-name__text").text
                                info['name'] = name
                            except Exception as es:
                                info['name'] = None

                            datas.append(info)

                        print(len(datas))
                        # print(href_list)

                            # print(link)
                    except (Exception, AttributeError) as ex:
                        print(ex)
                        return None
                else:
                    print(resp.status_code)
        
def get_product_data():
    with requests.Session() as session:
        i = 0
        for d in datas:
            i += 1
            useragent = UserAgent()
            headers = {
                    "accept": "*/*",
                    "user-agent": f"{useragent.random}",     
                    }
            with session.get(d["url"], headers=headers) as resp:
                # print(resp.status)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "lxml")
                    try:
                        wrapper = soup.find("article", class_="product-page-content__wrapper")
                        # name = wrapper.find('h1', class_="product-page-content__product-name").find_next().text
                        prod_id = wrapper.find("p", class_="product-page-content__article").text
                        d['id_product'] = prod_id
                    except Exception as ex:
                        d['id_product'] = None
                    try:
                        param = soup.find("div", class_="product-page-content__column--left")
                        lists = param.find("ul", class_="product-attributes__list style--product-page-short-list").find_all("li")
                        brand = lists[-1].find("a").text
                        d['brand'] = brand
                    except Exception as ex:
                        d['brand'] = None
                else:
                    print(f"Error: {resp.status_code}")
            print(f"{i}-ый пошел")

        

def main():
    url_metro = "https://online.metro-cc.ru/"
    url_card = "https://online.metro-cc.ru/category/chaj-kofe-kakao/chay?page="
    pages = 1
    get_product_href(url_card, pages)
    # with open("data/link.txt")
    get_product_data()
    with open("data/items.json", "w+") as f:
        json.dump(datas, f, indent=4, ensure_ascii=False)
    print(f"Данные записаны по пути 'data/items.json'")
    # print(len(href_list))



if __name__ == "__main__":
    main()