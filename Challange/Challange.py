import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from scrapy import Selector

def extracting_data(url):
    
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    driver.get(url)

    response = Selector(text = driver.page_source.encode('utf-8'))

    products = response.css(".sooqrSearchResults .innerproductlist .productlist-imgholder ::attr(href)").getall()
    
    if len(products) == 0:
        return "No products avilable with your requirements."
    
    produts_list = []
    for i in products:
        prod_specs = {}
        result = requests.get(i)
        response1 = Selector(result)
        price = response1.css(".buy-price .product-price-amount ::text").get()
        currency = response1.css(".buy-price .product-price-currency ::text").get()
        final_price = currency + " " + price
        final_price = final_price.replace(",",".")
        avilability = response1.xpath("normalize-space(//span[@class='stock-green'])").get()
        if avilability == None or avilability == "":
            avilability = "The item is no longer in the range."
        keys = response1.xpath("//div[@class='innerspecsholder']//div[@id='pdetailTableSpecs']//table//tr//td[1]/text()").getall()
        values = response1.xpath("//div[@class='innerspecsholder']//div[@id='pdetailTableSpecs']//table//tr//td[2]/text()").getall()
        needle_size = ""
        composition = ""
        if len(keys) > 0 and len(values) > 0:
            produt_specifications = dict(zip(keys, values))
            for specs_key, specs_value in produt_specifications.items():
                if "Nadelstärke" in specs_key:
                    needle_size = specs_value
                elif "Zusammenstellung" in specs_key:
                    composition = specs_value
        
        prod_specs['Price'] = final_price
        prod_specs['Avilablity'] = avilability
        prod_specs['Needle Size'] = needle_size
        prod_specs['Composition'] = composition
        produts_list.append(prod_specs)
    
    return produts_list

def selecting_products_and_brands():
    print("Names :   1) Natura XL   2) Safran  3) Baby Merino Mix   4) Alpacca Speciale   5) Special double knit ")
    name = input("Enter the produt Name Number like(1,2)")
    if name == "1":
        name = "Natura XL"
    elif name == "2":
        name = "Safran"
    elif name == "3":
        name = "Baby Merino Mix"
    elif name == "4":
        name = "Alpacca Speciale"
    elif name == "5":
        name = "Special double knit"
    else:
        name = "Wrong"

    print("Brands :   1) DMC   2) Drops  3) Drops   4) Hahn   5) Stylecraft  ")
    brand = input("Enter the Brand Name Number like(1,2)")
    if brand == "1":
        brand = "DMC"
    elif brand == "2":
        brand = "Drops"
    elif brand == "3":
        brand = "Drops"
    elif brand == "4":
        brand = "Hahn"
    elif brand == "5":
        brand = "Stylecraft"
    else:
        brand = "Wrong"
    
    return name, brand

if __name__ == '__main__':
    
    name, brand = selecting_products_and_brands()
    url = f"https://www.wollplatz.de/?#sqr:(q[{name}],f191640[{brand}])"
    produt_list = extracting_data(url)
    if type(produt_list) == str:
        print(produt_list)
    elif type(produt_list) == list:
        print(produt_list)