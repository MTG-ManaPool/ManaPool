from cardlist.cardlist import CardList
import pandas as pd
import webbrowser
import requests

class PurchaseList(CardList):

    def __init__(self, cardlist):
        self.cardlist = cardlist.cardlist.copy(deep=True)

    def submitOrder(self):

        #GET
        print('Submitting your order...')
        baseURL = "https://www.tcgplayer.com/massentry?productline=Magic&utm_campaign=affiliate&utm_medium=AFFILIATECODE&utm_source=AFFILIATECODE"
        encoding = "&c="
        for index, card in self.cardlist.iterrows():
            encoding += f"1{card['name'].replace(' ', '%20')}%20[{card['set'].replace(' ', '%20').upper()}]%7C%7C"
        
        url = baseURL + encoding
        webbrowser.open_new_tab(url)

        #POST
        # https://api.tcgplayer.com/massentry?partner=AFFILIATECODE&utm_campaign=affiliate&utm_medium=AFFILIATECODE&utm_source=AFFILIATECODE

        # print('Submitting your order...')
        # postURL = 'https://api.tcgplayer.com/massentry?partner=AFFILIATECODE&utm_campaign=affiliate&utm_medium=AFFILIATECODE&utm_source=AFFILIATECODE'
        # encoding = "&c="
        # for index, card in self.cardlist.iterrows():
        #     encoding += f"1{card['name'].replace(' ', '%20')}%20[{card['set'].replace(' ', '%20').upper()}]%7C%7C"

        # body = {'body': encoding} 
        # res = requests.post(postURL, data=body)
        # print(res.headers['Location'])
        # redirect = res.history
        # webbrowser.open_new_tab(redirect)

        placeholder = input('Press any key to continue...\n')