#################################################################################################################################
# This is a script that takes in a list of words in a language and creates an anki deck with the translation for practice and   #
# memorization of vocabulary                                                                                                    #
#                                                                                                                               #
# Dependencies                                                                                                                  #
# genanki                                                                                                                       #
# requests                                                                                                                      #
# libretranslate (either you can buy an API key or self host the translation API)                                               #
#                                                                                                                               #
#                                                                                                                               #
# Happy language learning journey.                                                                                                      #
#################################################################################################################################

import genanki
import requests
import sys
import os
import random

FROM_LANGUAGE = 'fr'
TO_LANGUAGE = 'en'

# TRANSLATE_API_URL = 'https://libretranslate.com/translate'

# uses self-hosted machine translation API
TRANSLATE_API_URL = 'http://127.0.0.1:5000/translate'

HEADERS = {
  "Content-Type": "application/json"
}

translation_dict = dict()


def main():
    # open wordlist using argument
    # argument error handling
    if len(sys.argv) != 2:
        print("usage: python main.py [filename]\n")
        sys.exit(1)


    if not os.path.isfile(sys.argv[1]):
        print("No file with that name.\nusage: python main.py [filename]\n")
        sys.exit(1)
        
    wordlist_file = sys.argv[1]
    wordlist_filename = os.path.splitext(wordlist_file)[0]

    with open(wordlist_file, 'r') as word_list:
        for word in iter(lambda: word_list.readline(), ''):
            word = word.rstrip()
            res = requests.post(TRANSLATE_API_URL,
                data=None,
                json= {
                    'q': word,
                    'source': FROM_LANGUAGE,
                    'target': TO_LANGUAGE,
                    'format': "text",
                    'alternatives': 3,
                    'api_key': ""
                },
            headers=HEADERS
            )
            
            data = res.json()
            translation_dict[word] = data['translatedText']


    # create a deck
    deck = genanki.Deck(
        deck_id=random.randint(1, 100000),
        name=wordlist_filename 
    )


    for word in translation_dict.keys():
        note = genanki.Note(
            model=genanki.BASIC_MODEL,
            fields=['{} ({})'.format(word, FROM_LANGUAGE), '{} ({})'.format(translation_dict[word], TO_LANGUAGE )]
        )
        
        note_reverse = genanki.Note(
            model=genanki.BASIC_MODEL,
            fields=['{} ({})'.format(translation_dict[word], TO_LANGUAGE ), '{} ({})'.format(word, FROM_LANGUAGE)]
        )
        
        deck.add_note(note)
        deck.add_note(note_reverse)
        

    genanki.Package(deck).write_to_file('{}.apkg'.format(wordlist_filename))

if __name__ == '__main__':
    main()
