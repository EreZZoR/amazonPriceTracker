import os
import time
import requests
import configparser
from colorama import *
from bs4 import BeautifulSoup
init()

class PriceSniper():
    def __init__(self):
        self.config = []
        self.webhook = []
        self.delay = 60
        self.productdelay = 5
        self.products = []
        self.start()
    
    def cls(self): os.system('cls' if os.name == 'nt' else 'clear')

    def checkfiles(self):
        if os.path.exists('config.ini') == False:
            self.cls()
            print(f'\n   {Fore.LIGHTRED_EX}Config file was not found, creating one...')
            with open('config.ini', 'w') as configfile:
                configfile.writelines(f'[Main]\ndelay = delay in minutes\nproduct-delay = delay in seconds\nwebhook = discord webhook url')
                configfile.flush()
            print(f'   {Fore.LIGHTGREEN_EX}Config file was created, change the settings then press any key!')
            input()
        
        if os.path.exists('products.txt') == False:
            self.cls()
            print(f'\n   {Fore.LIGHTRED_EX}Products file was not found, creating one...')
            with open('products.txt', 'w') as productsfile:
                productsfile.writelines('Write your product urls here, example:\nhttps://amazon.es/cock\nhttps://amazon.es/dang')
                productsfile.flush()
            print(f'   {Fore.LIGHTGREEN_EX}Products file was created, add your products then press any key!')
            input()
        
        self.cls()
        print(f'\n   {Fore.LIGHTCYAN_EX}All files were found, loading them...')
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.delay = int(self.config['Main']['delay'])*60
        self.productdelay = int(self.config['Main']['product-delay'])
        self.webhook = self.config['Main']['webhook']
        print(f'\n   {Fore.LIGHTGREEN_EX}Config loaded.')

        self.products = open('products.txt', 'r').read().splitlines()
        print(f'   {Fore.LIGHTGREEN_EX}Products loaded.')

    def sendwebhook(self, difference, productid, landingimage):
        headers = {'Content-Type': 'application/json'}

        embed = {
            'description': f'[Product Link!](https://amazon.es/dp/{productid})',
            'title': f'Lower price was found ({difference} eur lower)!',
            'image': {
            'url': landingimage
            }
            }

        data = {
            'content': '@everyone',
            'username': 'Dangg',
            'embeds': [
                embed
                ],
        }
        req = requests.post(self.webhook, json=data, headers=headers)

    def getprice(self, url):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "lxml")
        price = soup.find(class_='a-offscreen').get_text()
        landingimage = soup.find(id='landingImage')['src']
        price = price.replace('€', '')
        price = price.replace(',', '.')
        self.checkproduct(price, url, landingimage)

    def checkproduct(self, price, url, landingimage):
        productid = url[-10:]
        if os.path.exists(f'{productid}.txt') == False:
            print(f'\n   {Fore.LIGHTCYAN_EX}New product found! saving price.')
            self.saveprice(price, productid)
        else:
            self.checkprice(price, productid, landingimage)

    def saveprice(self, price, productid):
        with open(f'{productid}.txt', 'w') as productfile:
            productfile.write(price)
    
    def checkprice(self, newprice, productid, landingimage):
        oldprice = open(f'{productid}.txt', 'r').read()
        if float(oldprice) > float(newprice):
            difference = float(oldprice) - float(newprice)
            print(f'\n   {Fore.LIGHTGREEN_EX}Product with id {Fore.LIGHTYELLOW_EX}{productid}{Fore.LIGHTGREEN_EX} has a lower price than before ({difference} eur lower), congrats!')
            self.saveprice(newprice, productid)
            self.sendwebhook(difference, productid, landingimage)

        elif float(oldprice) == float(newprice):
            print(f'\n   {Fore.LIGHTCYAN_EX}Product with id {Fore.LIGHTYELLOW_EX}{productid}{Fore.LIGHTCYAN_EX} has the same price as before.')
        
        elif float(oldprice) < float(newprice):
            difference = float(newprice) - float(oldprice)
            print(f'\n   {Fore.LIGHTRED_EX}Product with id {Fore.LIGHTYELLOW_EX}{productid}{Fore.LIGHTRED_EX} has a higher price than before ({difference} eur higher) :(')
            self.saveprice(newprice, productid)

    def start(self):
        self.cls()
        self.checkfiles()
        time.sleep(1)
        self.cls()
        while True:
            for product in self.products:
                self.getprice(product)
                print(f'   {Fore.LIGHTCYAN_EX}Waiting delay({self.productdelay} seconds)...')
                time.sleep(self.productdelay)
            
            time.sleep(2)
            self.cls()
            print(f'\n   {Fore.LIGHTCYAN_EX}Waiting delay({int(self.delay/60)} minutes)...')
            time.sleep(self.delay)

if __name__ == '__main__':
    PriceSniper()