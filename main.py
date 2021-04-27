from selenium import webdriver
import random
import time
import csv


titles = []
prices = []
seller = []
shipping = []
images = []
urls = []
ratings = []
sold = []


def trimPageFromUrl(current_url):
    if(current_url.__contains__("&page")):
        return current_url[:-7]
    else:
        return current_url


def refreshPageIfnotFoundProducts():
    bika=False
    while not bika:
        time.sleep(1)
        try:
            web.find_element_by_class_name("list-item")
            bika=True
        except Exception:
            web.refresh()


def doScroll():
    web.execute_script("window.scrollTo(0, document.body.scrollHeight/10);")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(document.body.scrollHeight/10, 2*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(2*(document.body.scrollHeight/10), 3*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(3*(document.body.scrollHeight/10), 4*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(4*(document.body.scrollHeight/10), 5*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(5*(document.body.scrollHeight/10), 6*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(6*(document.body.scrollHeight/10), 7*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(7*(document.body.scrollHeight/10), 8*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(8*(document.body.scrollHeight/10), 9*(document.body.scrollHeight/10));")
    time.sleep(0.5)
    web.execute_script("window.scrollTo(9*(document.body.scrollHeight/10), 10*(document.body.scrollHeight/10));")
    time.sleep(0.5)


def runscrape(page):
    web.implicitly_wait(30)

    web.get(trimPageFromUrl(web.current_url)+"&page="+page.__str__())

    # Make a smooth scroll
    doScroll()

    items = web.find_elements_by_class_name("list-item")
    for item in items:
        titles.append(item.find_element_by_class_name("item-title").text)
        prices.append(item.find_element_by_class_name("price-current").text)
        seller.append(item.find_element_by_class_name("store-name").text)
        shipping.append(item.find_element_by_class_name("shipping-value").text)

        img=item.find_element_by_class_name("item-img")
        images.append(img.get_attribute("src"))

        tempurl = item.find_element_by_xpath(".//a[@target='_blank']")
        urls.append(tempurl.get_attribute("href"))

        sold.append(item.find_element_by_class_name("sale-value-link").text)

        tempratinig = item.find_element_by_class_name("item-sale-wrap").text.split("\n")
        ratings.append(tempratinig[0])
    print(len(items))


search = input("enter product to scrape:")

web = webdriver.Chrome("./chromedriver.exe")
url = "https://www.aliexpress.com/"
web.get(url)
time.sleep(5)
print(web.window_handles)
try:
    web.find_element_by_xpath("//a[@class='close-layer']").click()
except Exception:
    try:
        web.find_element_by_xpath("/html/body/div[5]/div/div/a").click()
    except Exception:
        print("add not found")
time.sleep(1)
email = "jimtrama@gmail.com"
password = "tramantzas"
web.find_element_by_name("SearchText").send_keys(search)
time.sleep(random.uniform(1,4))
web.find_element_by_class_name("search-button").click()
flag = False
try:
    time.sleep(random.uniform(1,4))
    web.find_element_by_xpath("//*[@id='fm-login-id']").send_keys(email)
    time.sleep(random.uniform(1,4))
    web.find_element_by_xpath("//*[@id='fm-login-password']").send_keys(password)
    time.sleep(random.uniform(1,4))
    web.find_element_by_xpath("//*[@id='login-form']/div[5]/button").click()
    time.sleep(4)
    refreshPageIfnotFoundProducts()

    try:
        web.find_element_by_xpath("//a[@role='button']").click()
    except Exception:
        try:
            web.find_element_by_xpath("/html/body/div[6]/div[2]/div/a").click()
        except Exception:
            web.find_element_by_xpath("/html/body/div[7]/div[2]/div/a").click()

except Exception:
    refreshPageIfnotFoundProducts()
    #doScroll()
    #availiable_pages = web.find_element_by_class_name("jump-aera").text.split(' ')
    #print("the availiable pages are : "+availiable_pages[1])
    max_pages=int(input("enter pages that you want to scarpe:"))
    flag = True
    refreshPageIfnotFoundProducts()
    for i in range(1,max_pages):
        print(i)
        try:
            runscrape(i)
        except Exception:
            print("Finished")

if(not flag):
    for i in range(1,max_pages):
        refreshPageIfnotFoundProducts()
        print(i)
        try:
            runscrape(i)
        except Exception:
            print("Finished")



csvfile=open('test.csv', 'a', newline='')
writer = csv.writer(csvfile)
writer.writerow(["Title", "Price", "Shipping Cost","Items Sold","Seller","Seller Rating","Url","Img Url"])
for i in range(0,len(titles)):
    writer.writerow([titles[i],prices[i],shipping[i],sold[i],seller[i],ratings[i],urls[i],images[i]])
print("Write to Excel successful")
csvfile.close()

