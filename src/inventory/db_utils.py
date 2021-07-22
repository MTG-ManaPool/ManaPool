import os
import requests

stock_headers = [
  ## Stock Count Headers
  "foil", # (Integer)
    # The current in stock count of foil versions of this card. 
  "nonfoil", # (Integer)
      # The current in stock count of nonfoil versions of this card. 

  # If card condition is chosen to be tracked in a future implementation one will need to consider the concepts such as:
  # near_mint_foil, near_mint_nonfoil.
  # lightly_played_foil, lightly_played_nonfoil.
  # moderately_played_foil, moderately_played_nonfoil.
  # heavily_played_foil, heavily_played_nonfoil.
  # damaged_foil, damaged_nonfoil.
]

schema_headers = stock_headers + [
  ## Unique Database ID
  "id", # (String)

  ## Visible Card Information
  "name", # (String) (e.g: 'Metallic Mimic')
    # A card can have the same name as another card, and is not unique. (Reprints)
    # A card may have a '//' to separate the front face name, from the back face name.
  "colors", # (String) (e.g: 'WUBRG')
    # A cards' color is determined by the colors present in it's mana cost.
    # A card mayhave no color, in which case it is an empty string.
    # A cards' color may contain any of the letters (non-repeating) 
        # 'W' - White
        # 'U', - Blue
        # 'B', - Black
        # 'R', - Red
        # 'G', - Green
  "color_identity", # (String) (e.g: 'UB')
    # A cards' color identity is the set of all mana colors that appear anywhere on the card.
    # A cards' color identity can be none. In which case, it is an empty string.
    # A cards' color identity may contain any of the letters (non-repeating).
        # 'W' - White Mana
        # 'U', - Blue Mana
        # 'B', - Black Mana
        # 'R', - Red Mana
        # 'G', - Green Mana
  "mana_cost", # (String) (e.g: {U}{B/U} // {R}{R/U})
    # Each bracketed symbol denotes a single Mana Value of the full mana cost.
    # A cards' Mana Cost may contain any of the letters (non-repeating).
      # 'W' - White Mana
      # 'U', - Blue Mana
      # 'B', - Black Mana
      # 'R', - Red Mana
      # 'G', - Green Mana
      # 'P', - Phyrexian Mana
      # 'X', - Variable  Mana
      # 'Y', - Variable  Mana
      # 'Z', - Variable  Mana
      # 'H', - Half Mana (Half the following mana cost)
    # A cards' Mana Cost may an integer from range 0 through 1,000,000.
    # A cards' Mana Cost may contain Hybrid Mana, which is any two Mana Costs separated by a '/'.
    # A cards' mana cost may have a ' // ' separating the front face cost, from the back face cost.
  "type_line", # (String) (e.g: 'artifact creature - shapeshifter')
    # A card always has a card type 
    # A card may have one or more subtypes. 
    # These are printed on the type line, separated by a '-'. 
  "set_type", # (String)
    # A cards' set type is a description of the type of Expansion set.
    # A cards' set type can be any of the following: 
      # 'vanguard'
      # 'masters'
      # 'treasure_chest'
      # 'core'
      # 'spellbook'
      # 'draft_innovation'
      # 'planechase'
      # 'memorabilia'
      # 'token'
      # 'expansion'
      # 'duel_deck'
      # 'starter'
      # 'promo'
      # 'from_the_vault'
      # 'premium_deck'
      # 'commander'
      # 'masterpiece'
      # 'box'
      # 'archenemy'
      # 'funny'
  "set_name", # (String) 
    # A card's set name is a full length string name for the Expansion set it can be found in.
  "rarity", # (String)
    # A cards' rarity can be one of the following:
      # common
      # uncommon
      # rare
      # mythic
      # bonus
      # special
  "artist", # (String)
    # A cards' artist is a string name of the author who drew the picture art of the card.
    # A cards' artist may not exist, in which case it is an empty string.
  "flavor_text", # (String)
    # A cards' flavor text is a long string that serves to provide a mood or give background information on the game world, but has no effect on gameplay.
    # A card may have no flavor text, in which case it is an empty string.
  "cmc", # (Float)
    # A cards' converted mana cost is the numeric value of all the mana in its Mana Cost.
    # A card can have a cmc of the following: 
      # 0.0
      # 0.5
      # 1.0
      # 2.0
      # 3.0
      # 4.0
      # 5.0
      # 6.0
      # 7.0
      # 8.0
      # 9.0
      # 10.0
      # 11.0
      # 12.0
      # 13.0
      # 14.0
      # 15.0
      # 16.0
      # 1000000.0
  "power", # (String)
    # A cards' power is the first number printed before the slash on the lower right-hand corner of creature cards.
    # A cards' power can be any of the following variables:
      # Combinable: '+1', 
      # Negative: '-1',
      # Dependent: '*',
      # Variable: '?',
      # Infinity: '∞',
      # Squared: '*²',
      # Additive and Variable: '2+*'
  "toughness", # (String)
    # A cards' toughness is the second number printed after the slash on the lower right-hand corner of creature cards.
    # A cards' toughness can be any of the following variables:
      # Combinable: '+1', 
      # Negative: '-1',
      # Dependent: '*',
      # Variable: '?',
      # Infinity: '∞',
      # Squared: '*²',
      # Negative and Variable: '7-*'
  "multiverse_ids", # (List) -> (Integer)  
    # A cards' multiverse ID is the unique ID given by the Gather site.
    # A card may not have a Gather ID, because it may not be intended for playing.
  "keywords",   # (List) -> (String) concatenated and comma separated.
    # A card may have a list of keyword affects that appear on the card.
    # A keyword is a special word, that gives a card special abilities/affects/meaning. 
  "image_uris", # (Dict) -> Extracted inner data into new headers, then dropped.
  "card_faces", # (Dict) -> Extracted inner data into new headers, then dropped.

  "set", # (String) 
    # A card's set is a 3-4 letter short-hand notation for the name of the Expansion set it can be found in.
  "collector_number", # (String)
    # A card has a unique number, or string pattern (usually containing a number) indicating it's linear order in an a specific set of cards.

  ## Additional Card Information
  # A card can can have one or more of these properties.
  # A card's uniqueness is determined by the set/collection_number of the card, not these properties.
  "layout", # (String) 
    # A cards' layout is a description of how the art and information is organized on the card.
    # A cards' layout can be any of the following:
      # 'vanguard'
      # 'modal_dfc'
      # 'saga'
      # 'host'
      # 'art_series'
      # 'transform'
      # 'double_faced_token'
      # 'token'
      # 'adventure'
      # 'class'
      # 'normal'
      # 'meld'
      # 'emblem'
      # 'split'
      # 'leveler'
      # 'planar'
      # 'augment'
      # 'flip'
      # 'scheme'
  "full_art", # (Boolean) 
  "textless", # (Boolean) 
  "oversized", # (Boolean) 
  "promo", # (Boolean) 
]

def getBulkData(requested_data):
    '''Programmatically retrieves the requested Scryfall Bulk Data JSON file.'''
    resp = requests.get("https://api.scryfall.com/bulk-data")
    available_bulk_data = resp.json()

    for bulk_file in available_bulk_data['data']:
        if(bulk_file['type'] == requested_data):
            scryfall_bulk_data_url = bulk_file['download_uri']
            break

    output_file = f'{requested_data}.json'
    # JSON Bulk File is large, and must be processed in chunks.
    # Optimal chunk size can be tested/configured later.
    with requests.get(scryfall_bulk_data_url, stream=True) as resp:
        with open(output_file, 'wb') as file:
            for chunk in resp.iter_content(chunk_size=8192):
                file.write(chunk)
    return os.path.realpath(output_file)