import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

df = pd.read_csv(r'D:\Absolut Products Price List.csv')
df = pd.DataFrame(df)
info = {"Product_Name":[], "Product_Price":[], "Retailer": [], "Reference":[]}


def getPriceSainbury(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    driverWaitForSainsburys(driver)
    name = driver.find_elements(By.CLASS_NAME, "pd__header")[0].text
    price = "£" + driver.find_elements(By.CLASS_NAME, "pd__cost")[0].find_elements(By.TAG_NAME, "div")[0].text.split("£")[1]
    info = {'Product': name, 'Price': price}
    return info

def getPriceWaitrose(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)  
    price = driver.find_elements(By.CLASS_NAME, "productPricing___3g80a")
    price = price[0].find_element(By.TAG_NAME, "span").text
    name = driver.find_elements(By.CLASS_NAME, "title___31Yu2")
    name = name[0].find_element(By.TAG_NAME, "span").text
    info = {'Product': name, 'Price': price}
    return info

def getPriceOcado(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    driverWaitForOcado(driver)
    name = driver.find_elements(By.CLASS_NAME, "bop-title")[0].find_elements(By.TAG_NAME, "h2")[0].text
    price = driver.find_elements(By.CLASS_NAME, "bop-price__wrapper")[0].find_elements(By.TAG_NAME, "h2")[0].text
    info = {'Product': name, 'Price': price}
    return info

def getPriceTesco(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    driverWaitForTesco(driver)
    name = driver.find_elements(By.CLASS_NAME, "product-details-tile__title")[0].text
    price = driver.find_elements(By.CLASS_NAME, "price-control-wrapper")[0].text
    info = {'Product': name, 'Price': price}
    return info

def getPriceASDA(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    driverWaitForASDA(driver)
    name = driver.find_elements(By.CLASS_NAME, "pdp-main-details__title")[0].text
    price = driver.find_elements(By.CLASS_NAME, "pdp-main-details__price")[0].text[4:]
    info = {'Product': name, 'Price': price}
    return info

def getPriceMorrisons(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    driverWaitForMorrisons(driver)
    name = driver.find_elements(By.CLASS_NAME, "bop-title")[0].find_elements(By.TAG_NAME, "h2")[0].text
    price = driver.find_elements(By.CLASS_NAME, "bop-price__current ")[0].text
    info = {'Product': name, 'Price': price}
    return info

def getPriceAmazon(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    driverWaitForAmazon(driver)
    name = driver.find_elements(By.ID, "productTitle")[0].text
    price_symbol = driver.find_elements(By.CLASS_NAME, "a-price-symbol")[0].text
    price_whole = driver.find_elements(By.CLASS_NAME, "a-price-whole")[0].text
    price_decimal = driver.find_elements(By.CLASS_NAME, "a-price-fraction")[0].text
    price = price_symbol + '' + price_whole + '.' + price_decimal
    info = {'Product': name, 'Price': price}
    return info


def driverWaitForSainsburys(driver):
    try:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'pd__cost')))
    except:
        print("Sainsburys page never loaded")

        
def driverWaitForWaitrose(driver):
    try:
        element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "productPricing___3g80a")))
    except:
        print("Waitrose page never loaded")

        
def driverWaitForOcado(driver):
    try:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'bop-price__wrapper')))
    except:
        print("Ocado page never loaded")


def driverWaitForTesco(driver):
    try:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "product-details-tile__title")))
    except:
        print("Tesco page never loaded")


def driverWaitForASDA(driver):
    try:
        element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'pdp-main-details__price-container')))
    except:
        print("ASDA page never loaded")


def driverWaitForMorrisons(driver):
    try:
        element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'bop-title')))
    except:
        print("Morrisons page never loaded")


def driverWaitForAmazon(driver):
    try:
        element = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, "a-section.a-spacing-none.aok-align-center")))
    except:
        print("Amazon page never loaded")

def csvExport(info):
    df = pd.DataFrame(info)
    df.to_csv (r'D:\Live prices4.csv', encoding="utf-8", index = False, header=True)

for index, link_addresses in df.iterrows():
    for link_address in link_addresses:
            if len(re.findall("www.sainsburys.co.uk/gol-ui/product/", str(link_address))) > 0:
                try:
                    product = getPriceSainbury(link_address)
                    info["Product_Name"].append(product["Product"])
                    info["Product_Price"].append(product["Price"])
                    info["Retailer"].append("Sainsburys")
                    info["Reference"].append(link_address)
                except:
                    print("Failed to get product price Sainsbury")
                    
            if len(re.findall( "www.tesco.com/groceries/en-GB/products/", str(link_address))) > 0:
                try:
                    product = getPriceTesco(link_address)
                    info["Product_Name"].append(product["Product"])
                    info["Product_Price"].append(product["Price"])
                    info["Retailer"].append("Tesco")
                    info["Reference"].append(link_address)
                except:
                    print("Failed to get product price Tesco")

            if len(re.findall( "www.waitrose.com/ecom/products/", str(link_address))) > 0:
                try:
                    product = getPriceWaitrose(link_address)
                    info["Product_Name"].append(product["Product"])
                    info["Product_Price"].append(product["Price"])
                    info["Retailer"].append("Waitrose")
                    info["Reference"].append(link_address)
                except:
                    print("Failed to get product price Waitrose")                   

            if len(re.findall( "groceries.asda.com/product/", str(link_address))) > 0:
                try:
                    product = getPriceASDA(link_address)
                    info["Product_Name"].append(product["Product"])
                    info["Product_Price"].append(product["Price"])
                    info["Retailer"].append("ASDA")
                    info["Reference"].append(link_address)
                except:
                    print("Failed to get product price ASDA")
                    
            if len(re.findall( "groceries.morrisons.com/products/", str(link_address))) > 0:
                try:
                    product = getPriceMorrisons(link_address)
                    info["Product_Name"].append(product["Product"])
                    info["Product_Price"].append(product["Price"])
                    info["Retailer"].append("Morrisons")
                    info["Reference"].append(link_address)
                except:
                    print("Failed to get product price Morrisons")   
                    
            if len(re.findall( "www.ocado.com/products/", str(link_address))) > 0:
                try:
                    product = getPriceOcado(link_address)
                    info["Product_Name"].append(product["Product"])
                    info["Product_Price"].append(product["Price"])
                    info["Retailer"].append("Ocado")
                    info["Reference"].append(link_address)
                except:
                    print("Failed to get product price Ocado")

            if len(re.findall( "www.amazon.co.uk/", str(link_address))) > 0:
                try:
                    product = getPriceAmazon(link_address)
                    info["Product_Name"].append(product["Product"])
                    info["Product_Price"].append(product["Price"])
                    info["Retailer"].append("Amazon")
                    info["Reference"].append(link_address)
                except:
                    print("Failed to get product price Amazon")  
                    
csvExport(info)
