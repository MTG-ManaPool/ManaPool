from cardlist.cardlist import CardList
import pandas as pd
import requests

class PurchaseList(CardList):

    def __init__(self, cardlist):
        self.cardlist = cardlist.copy(deep=True)

    def submitOrder(self):
        print('Submitting your order...')
        # 'https://api.tcgplayer.com/massentry?partner=AFFILIATECODE&utm_campaign=affiliate&utm_medium=AFFILIATECODE&utm_source=AFFILIATECODE'
        placeholder = input('Press any key to continue...\n')