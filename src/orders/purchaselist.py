from cardlist.cardlist import CardList
import pandas as pd
import requests

class PurchaseList(CardList):

    def __init__(self, cardlist):
        self.cardlist = cardlist.copy(deep=True)

    def submitOrder(self):
        print('Submitting your order...')
        baseURL = "https://www.tcgplayer.com/massentry?productline=Magic&utm_campaign=affiliate&utm_medium=AFFILIATECODE&utm_source=AFFILIATECODE"
        encoding = "&c=1%20Nissa,%20Steward%20of%20Elements||4%20Chart%20a%20Course||"
        placeholder = input('Press any key to continue...\n')