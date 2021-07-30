from inventory.inventory import MP_Inventory as Inventory
from database.database import MP_Database as Database
from ui.menu import Menu

def main():
    # Set up db
    try:
        database = Database()
        inventory = Inventory()
        menu = Menu()
        menu.mainMenu(inventory, database)
    except Exception as e:
        print(e)
    exit()
    inventory.close()
main()