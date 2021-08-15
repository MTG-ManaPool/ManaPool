import unittest
import pandas
from database.database import MP_Database
from unittest import mock

class TestDatabase(unittest.TestCase):

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
        return super().setUp()

    @mock.patch("pandas.read_sql_query")
    def test_all_cards_returns_cards(self, mock_read_sql_query):
        print("TestDatabase - test_all_cards_returns_cards")
        self.database.all_cards()
        query = f"SELECT * FROM '{self.table_name}'"
        mock_read_sql_query.assert_called_once_with(query, self.test_db_connection)
        # TODO: Test size of return == size we expect

    # def test_search_By_MID(self, card_mid):
    #     print("TestDatabase - test_search_By_MID")

    # def test_search_By_Name(self, cardname):
    #     print("TestDatabase - test_search_By_Name")

    def test_search_by_set_finds_cards(self):
        print("TestDatabase - test_search_by_set_finds_cards")
        set_name = "Time Spiral"
        cards = self.test_db_connection.execute(f"SELECT * FROM '{self.table_name}' WHERE set_name='{set_name}'").fetchall()
        self.assertIsNotNone(cards)
        for card in cards:
            self.assertEqual(set_name, card['set_name'])
        
    def test_search_by_set_fails(self):
        print("TestDatabase - test_search_by_set_fails")
        set_name = "Time Spiral"
        cards = self.test_db_connection.execute(f"SELECT * FROM '{self.table_name}' WHERE set_name='{set_name}'").fetchall()
        self.assertIsNotNone(cards)
        for card in cards:
            self.assertNotEqual("Time Spira", card['set_name'])

    def test_search_by_set_returns_empty(self):
        print("TestDatabase - test_search_by_set_returns_empty")
        set_name = "bad entry"
        cards = self.test_db_connection.execute(f"SELECT * FROM '{self.table_name}' WHERE set_name='{set_name}'").fetchall()
        self.assertEqual(len(cards), 0)
        self.assertEqual(cards, [])

    def tearDown(self) -> None:
        #os.remove(self.database_name)
        return super().tearDown()