import requests
import pandas

class Scryfall():

    def __init__(self):
        self._cache = pandas.DataFrame()

    # PUBLIC
    # queries current cache for recent searches, limits scryfall db queries
    def queryCache(self, query):
        if query in self._cache:
            return True
        return False

    # search function entry point, takes a string query and a string search type
    def search(self, query, type):
        if type == 'set':
            setcode = self._getSetCode(query[0])
            self._queryBySet(setcode)

        if type == 'block':
            self._queryByBlock(query[0])

        if type == 'fuzzyname':
            self._queryByFuzzyName(query[0])

        if type == 'm_id':
            self._queryByMID(query[0])

    # PRIVATE
    # compares query text against known sets returning set code, increases likelyhood of a valid search
    def _getSetCode(self, query):

        if len(query) == 3:
            return query

        # CORE SETS
        if '10' in query:
            return 'M10'
        elif '11' in query:
            return 'M11'
        elif '12' in query:
            return 'M12'
        elif '13' in query:
            return 'M13'
        elif '14' in query:
            return 'M14'
        elif '15' in query:
            return 'M15'
        elif '19' in query:
            return 'M19'
        elif '20' in query:
            return 'M20'
        elif '21' in query:
            return 'M21'
        # CORE SETS:LIMITED
        elif 'ALPHA' in query.upper():
            return 'LEA'
        elif 'BETA' in query.upper():
            return 'LEB'
        elif 'UNLIMITED' in query.upper():
            return '2ED'
        elif 'REVISED' in query.upper():
            return '3ED'
        elif 'FOURTH' in query.upper() or 'IV' in query.upper(): # Potential bug if 'V' returns true, could return 4ED when 5ED desired
            return '4ED'
        elif 'FIFTH' in query.upper() or 'V' in query.upper():
            return '5ED'
        elif 'SIXTH' in query.upper() or 'VI' in query.upper():
            return '6ED'
        elif 'SEVENTH' in query.upper() or 'VII' in query.upper():
            return '7ED'
        elif 'EIGHTH' in query.upper() or 'VIII' in query.upper():
            return '8ED'
        elif 'NINTH' in query.upper() or 'IX' in query.upper():
            return '9ED'
        elif 'TENTH' in query.upper() or 'X' in query.upper():
            return '10E'
        # EXPANSION SETS
        elif 'ARABIAN' in query.upper():
            return 'ARN'
        # ...
        elif 'WAR' in query.upper() or 'SPARK' in query.upper():
            return 'WAR'
        elif 'THRONE' in query.upper() or 'ELDRAINE' in query.upper():
            return 'ELD'
        elif 'THEROS' in query.upper(): 
            return 'THB'
        elif 'IKORIA' in query.upper() or 'BEHEMOTHS' in query.upper():
            return 'IKO'
        elif 'IKORIA' in query.upper() or 'BEHEMOTHS' in query.upper():
            return 'IKO'
        elif 'ZENDIKAR' in query.upper():
            if 'RISING' in query.upper():
                return 'ZNR'
            elif 'BATTLE' in query.upper():
                return 'BFZ'
        elif 'KALDHEIM' in query.upper():
            return 'KHM'
        elif 'STRIXHAVEN' in query.upper():
            return 'KHM'
        
        return query

    # queries scryfall db by setcode, returns list of card dicts 
    def _queryBySet(self, set):
        print('\n\nQuerying scryfall db by set name...\n\n')
        try:
            res = requests.get(f'https://api.scryfall.com/sets/{set}')
            print(res)
            placeholder = input('Press any key to continue...\n>>')
        except Exception as e:
            print(e)
            placeholder = input('Press any key to continue...\n>>')
    
    # UNFINISHED
    def _queryByBlock(self, block):
        print('\n\nQuerying scryfall db by block name...\n\n')
        print(block)
        # res = requests.get(f'https://api.scryfall.com/blocks/{block}')
        placeholder = input('Press any key to continue...\n>>')

    def _queryByFuzzyName(self, fuzzyname):
        print('\n\nQuerying scryfall db by fuzzy name...\n\n')
        print(fuzzyname)
        # res = requests.get(f'https://api.scryfall.com/blocks/{fuzzyname}')
        placeholder = input('Press any key to continue...\n>>')

    def _queryByMID(self, id):
        print(id)
        print('\n\nQuerying scryfall db by multiverse id..\n\n')
        placeholder = input('Press any key to continue...\n>>')

    def _scryfallDataWash(self, scryfall_data):
        print('\n\nReformatting scryfall data for local storage')
