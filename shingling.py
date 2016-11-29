# ======== shingling ========
# This code represent each document as a set of shingles.
# The shingles are formed by combining K consecutive characters together.
# Shingles are mapped to shingle IDs using some hash function.

import io
import os
import re
import time
import binascii
import unicodedata
from bs4 import BeautifulSoup

import definitions

SHINGLE_LENGTH = 10


# Scraping function that extract information from recipes.
def scraping(filename):

    def check_not_null(feature):
        if len(feature) > 0:
            return feature[0].text.strip()
        else:
            return u''

    # open the recipes folder
    f = io.open(definitions.RECIPES_FOLDER + '/' + filename, 'r', encoding='utf-8')
    # set the scraper (using the lxml parser)
    soup = BeautifulSoup(f, 'lxml')

    # find the attributes and check them if are empty
    title = check_not_null(soup.find_all("h1", class_='content-title__text'))
    author = check_not_null(soup.find_all("a", class_='chef__link'))
    prepTime = check_not_null(soup.find_all("p", class_='recipe-metadata__prep-time'))
    cookTime = check_not_null(soup.find_all("p", class_='recipe-metadata__cook-time'))
    serving = check_not_null(soup.find_all("p", class_='recipe-metadata__serving'))
    dietary = check_not_null(soup.find_all("div", class_='recipe-metadata__dietary'))

    ingredients = check_not_null(soup.find_all("div", class_='recipe-ingredients-wrapper'))
    ingredients = re.sub('\s+', ' ', ingredients.strip().lstrip('Ingredients').lstrip())

    method = check_not_null(soup.find_all("div", class_='recipe-method-wrapper'))
    method = re.sub('\s+', ' ', method.strip().lstrip('Method').lstrip())

    f.close()

    aggr = title + '\n' + ingredients + '\n' + author + '\n' + prepTime + '\n' + \
           cookTime + '\n' + serving + '\n' + method + '\n' + dietary
    aggr = unicodedata.normalize('NFKD', aggr).encode('ASCII', 'ignore')
    return aggr


# Shingling function that shingle all documents by K characters and hash them.
def shingling(list_of_files, scraping_function):
    print 'Shingling Documents...'

    # Create a dictionary of the documents, mapping the document identifier to the list of
    # shingle IDs that appear in the document.
    docShingleSets = dict()
    # Maintain a list of all document IDs
    docNames = list()

    t0 = time.time()

    for filename in list_of_files:
        # Read all the strings in the document.
        docstring = scraping_function(filename)

        # Retrieve the recipe ID, which is the file name.
        docID = filename
        docNames.append(docID)

        # 'shinglesInDoc' will hold all the unique shingle IDs present in the current
        # document. If a shingle ID occurs multiple times in the document, it will only
        # appear once in the set (we'll use the propery of Python sets).
        shinglesInDoc = set()

        # For each K character in the document
        for i in range(len(docstring) - SHINGLE_LENGTH + 1):
            # Construct the shingle
            shingle = docstring[i:i + SHINGLE_LENGTH]

            # Hash the shingle to a 32-bit integer
            crc = binascii.crc32(shingle) & 0xffffffff

            # Add the hash value to the list of shingles for the current document.
            # Note that set objects will only add the value to the set if the set doesn't
            # already contain it.
            shinglesInDoc.add(crc)

        # Store the completed list of shingles for this document in the dictionary.
        docShingleSets[docID] = shinglesInDoc
    t1 = time.time()
    print 'Time to Shingling %d documents by %d characters: %f' % (len(list_of_files),
                                                                   SHINGLE_LENGTH,
                                                                   t1 - t0)
    return docShingleSets

if __name__ == '__main__':
    files = os.listdir(definitions.RECIPES_FOLDER)
    print shingling(files[:10], scraping)
