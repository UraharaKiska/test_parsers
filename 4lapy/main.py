import bs4 
import lxml
import requests
from fake_useragent import UserAgent
import json

useragent = UserAgent()
headers = {
    "accept": "*/*",
    "user-agent": f"{useragent.random}",     
        }

def get_id(url):
    with requests.Session() as session:
        with session.get(url, headers=headers) as resp:
            if resp.status_code == 200:
                with open("data.json", "w+") as f:
                    data = json.dumps(resp.json())
                    json.dump(data, f, ensure_ascii=False, indent=4)
                dict_info = json.loads(data)
                id_list = []
                for d in dict_info:
                    id_list.append(d['ItemId'])
                # with open("ItemId.txt", "w+") as f:
                #     for i in id_list:
                        # f.write(f"{str(i)}\n")
                return id_list
            else:
                print("can't connect to the site")
        

def get_product_data(url):
    with requests.Session() as session:
        with session.get(url, headers=headers) as resp:
            if resp.status_code == 200:
                data = json.dumps(resp.json())
                data = resp.json()
                result = []
                for d in data:
                    r = {}
                    r['id'] = d['ItemId']
                    r['name'] = d['Name']
                    r['url'] = d['Url']
                    r['current_price'] = d['Price']
                    r['old_price'] = d['OldPrice']
                    r['brand'] = d['Vendor']
                    result.append(r)
                with open("data/product_info.json", "w+") as f:
                    # data = json.dumps(result)
                    json.dump(result, f, ensure_ascii=False, indent=4)

            else:
                print('Error')

# def get_product(utl)
def main():
    cat_id = 3
    url_id = f"https://api.retailrocket.ru/api/2.0/recommendation/popular/5b151eb597a528b658db601e/?&categoryIds={cat_id}&format=json"
    url_product = "https://api.retailrocket.ru/api/1.0/partner/5b151eb597a528b658db601e/items/?itemsIds="
    id_list = get_id(url_id)
    for i in id_list:
        url_id += f"{i},"
    if id_list is not None:
       get_product_data(url_id) 
    else:
        print("No data")


if __name__ == "__main__":
    
    main()