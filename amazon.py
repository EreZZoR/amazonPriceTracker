import requests
from bs4 import BeautifulSoup
import mail
from time import sleep

URL = "https://www.amazon.es/Panasonic-Lumix-DMC-FZ300EG-K-estabilizador-Grabaci%C3%B3n/dp/B0127HAGK2/ref=sr_1_3?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=fz300&qid=1593973490&sr=8-3"
HEADER = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

def getprice() :
    page = requests.get(URL, headers = HEADER)
    soup = BeautifulSoup(page.content, "lxml")
    price = soup.find(id="priceblock_ourprice").get_text()
    price = price[:-2]
    price = price.replace(",",".")
    return price

def readFile() :
    f = open("price.txt", "r")
    if f.mode == "r":
        content = f.read()
    f.close()
    return content

def writeFile(number) :
    f = open("price.txt", "w")
    if f.mode == "w":
        f.write(number)
    f.close()

def main() :
    try:
        open("price.txt")
    except FileNotFoundError:
        writeFile(getprice())

    while(True):
        oldprice = readFile()
        newprice = getprice()

        if float(newprice) < float(oldprice) - 10 :
            message = "Su producto ha sido rebajado a " + str(newprice) + " euros. \n" + "URL: " + str(URL)
            mail.sendemail(message)
            writeFile(newprice)
            print("Mail sent \n")

        sleep(3600)    

if __name__ == "__main__":
    main()

