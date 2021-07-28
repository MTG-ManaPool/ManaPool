# ManaPool - Magic the Gathering Collection Tool

Stevon Shaw, Trevor Johnson, Victor Heredia  - 2021

## What is ManaPool?

- - -

ManaPool is a collection manager and acquisition tool for Magic the Gathering trading cards.

ManaPool provides an interface to manage and search a digital collection of Magic the Gathering cards.

ManaPool builds purchase orders from your existing collection, allowing you to quickly find the cards you need.

ManaPool searches popular digital card stores, to find the best price available for your purchase order.


## Roadmap to MVP

---

- [x] Gather a collection of card data

- [x] Implement an inventory system using card data.

- [ ] Provide a user-friendly UI for interfacing with the IMS.

- [ ] Export groups of cards as lists for purchase orders online.

- [ ] And further beyond. . .

## Install

- - -

For ManaPool, you will need python3, and pip. It is recommended to use a virtual environment as well:

    sudo apt-get install python3 python3-pip virtualenv

Fetch the latest version of the project:

    git clone https://github.com/MTG-ManaPool/ManaPool.git

Activate your virtual environment:

### Unix

    virtualenv env
    source env/bin/activate

### Windows

    virtualenv env
    .\env\Scripts\activate

Then install the requirements:

    pip install -r requirements.txt

## Run

    python src/main.py

## License

- - -
This work is made available under the "MIT License".
Please see the file LICENSE in this distribution for license terms.
- - -

ManaPool is not approved/endorsed by Wizards of the Coast.  
Portions of ManaPool are unofficial Fan Content permitted under the Fan Content Policy.  
The literal and graphical information presented in this application about Magic: The Gathering, including card images, mana symbols, and Oracle text, are copyright Wizards of the Coast.  ©Wizards of the Coast LLC. 
