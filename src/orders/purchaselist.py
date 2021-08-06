from cardlist.cardlist import CardList
import copy

class PurchaseList(CardList):

    def __init__(self, cardlist):
        self.cardlist = copy.deepcopy(cardlist)

    def submitOrder(self):
        print('Submitting your order...')
        placeholder = input('Press any key to continue...\n')