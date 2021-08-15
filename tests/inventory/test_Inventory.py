import unittest
import pandas
from database.database import MP_Database
from inventory.inventory import MP_Inventory
from unittest import mock


class TestInventory(unittest.TestCase):
    def setUp(self) -> None:
        # Create 60k DB
        # self.database = MP_Database()
        self.database_name = "test_database.db"
        self.table_name = "MTG-Cards"
        self.database = MP_Database(self.database_name)
        self.test_db_connection =   self.database.connection
        
        schema = [ 'index', 'foil', 'nonfoil', 'id', 'name', 'colors', 'color_identity',
            'mana_cost', 'type_line', 'set_type', 'set_name', 'rarity', 'artist',
            'flavor_text', 'cmc', 'power', 'toughness', 'multiverse_ids',
            'keywords', 'set', 'collector_number', 'layout', 'full_art', 'textless',
            'oversized', 'promo', 'small_img', 'normal_img', 'large_img', 'png_img',
            'art_crop_img', 'border_crop_img']

        card = pandas.read_sql_query(f"SELECT * FROM '{self.table_name}' LIMIT 1", self.test_db_connection)
        self.assertListEqual(list(card.columns), schema)
        self.test_inventory = MP_Inventory()
        return super().setUp()

    @mock.patch("pandas.read_sql_query", return_value=None)
    def test_get_inventory(self, mock_read_sql_query):
        print('TestInventory - test_search_before_add')
        cards = self.test_inventory.getInventory()
        query = f"SELECT * FROM '{self.table_name}' WHERE foil > 0 OR nonfoil > 0;"
        mock_read_sql_query.assert_called_once_with(query, self.test_db_connection)
    
    @mock.patch("pandas.read_sql_query", return_value=None)
    def test_inv_search_by_set(self, mock_read_sql_query):
        print("TestDatabase - test_search_by_set_finds_cards")
        set_name = "Time Spiral"
        _cards = self.test_inventory.searchBySet(set_name)
        query = f"SELECT * FROM '{self.table_name}' WHERE set_name='{set_name}' AND (foil>0 OR nonfoil>0) ORDER BY multiverse_ids;"
        mock_read_sql_query.assert_called_once_with(query, self.test_db_connection)

    @mock.patch("pandas.read_sql_query", return_value=None)
    def test_inv_search_by_name(self, mock_read_sql_query):
        print("TestDatabase - test_search_by_name_finds_cards")
        card_name = "Fury Sliver"
        _cards = self.test_inventory.searchByName(card_name)
        query = f"SELECT * FROM '{self.table_name}' WHERE name LIKE '%{card_name}%' AND (foil>0 OR nonfoil>0) ORDER BY multiverse_ids;"
        mock_read_sql_query.assert_called_once_with(query, self.test_db_connection)
    
    @mock.patch("pandas.read_sql_query", return_value=None)
    def test_inv_search_by_mid(self, mock_read_sql_query):
        print("TestDatabase - test_search_by_mid_finds_cards")
        card_mid = "109722"
        _cards = self.test_inventory.searchByMID(card_mid)
        query = f"SELECT * FROM '{self.table_name}' WHERE multiverse_ids='{card_mid}' AND (foil>0 OR nonfoil>0) ORDER BY multiverse_ids;"
        mock_read_sql_query.assert_called_once_with(query, self.test_db_connection)

    def test_add_to_inventory(self):
        print('TestInventory - test_add_to_inventory')