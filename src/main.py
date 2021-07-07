from inventory.Inventory import Inventory
from ui.menu import menu

def main():
    # Set up db
    inventory = Inventory()
    menu(inventory)
    exit()

main()