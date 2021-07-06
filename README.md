# ManaPool - Magic the Gathering Collection Tool

Stevon Shaw, Trevor Johnson, Victor Heredia  - 2021

## What is ManaPool?

- - -

ManaPool is a collection manager and aquisition tool for Magic the Gathering trading cards.

ManaPool provides an interface to manage a digital representation of a personal collection of Magic the Gathering cards.

ManaPool assists with aquiring sets of cards, by searching popular digital stores, to complie a purchase order with the best price available.


## Roadmap to MVP

---

- [x] Gather a collection of card data

- [ ] Implement an inventory system using card data.

- [ ] Provide a user-friendly UI for interfacing with the IMS.

- [ ] Export groups of cards as lists for purchase orders online.

- [ ] And further beyond. . .

## Install

- - -

For ManaPool, you will need python3, and pip. It is recommended to use a virtual environment as well:

    sudo apt-get install python3 python3-pip virtualenv

Fetch the latest version of the project:

    git clone https://github.com/MTG-ManaPool/ManaPool.git

Activate your virtual environment,

### Unix

    virtualenv env
    source env/bin/activate

### Windows

    virtualenv env
    .\env\Scripts\activate

Then install the requirements:

    pip install -r requirements.txt

## License

- - -
This work is made available under the "MIT License".
Please see the file LICENSE in this distribution for license terms.
