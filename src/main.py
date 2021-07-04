from inventory.inventory import Inventory
from ui.menu import menu
from scryfall.scryfall import Scryfall
from inventory.inventory import Inventory

def main():
    # Set up db
    scryfall = Scryfall()
    inventory = Inventory()
    menu(scryfall, inventory)
    exit()

main()