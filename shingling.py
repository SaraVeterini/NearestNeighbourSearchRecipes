# ======== shingling ========
# This code represents each document as a set of shingles.
# The shingles are formed by combining K consecutive characters together.
# Shingles are mapped to shingle IDs using some hash function.

import io
import os
import re
import time
import string
import hashlib
import unicodedata
from bs4 import BeautifulSoup

# import sys
# sys.path.append('utils')
from utils.loader import save_binary_file, load_binary_file


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
    description = check_not_null(soup.find_all("div", class_='recipe-description'))

    ingredients = check_not_null(soup.find_all("div", class_='recipe-ingredients-wrapper'))
    ingredients = re.sub('\s+', ' ', ingredients.strip().lstrip('Ingredients').lstrip())

    method = check_not_null(soup.find_all("div", class_='recipe-method-wrapper'))
    method = re.sub('\s+', ' ', method.strip().lstrip('Method').lstrip())

    f.close()

    aggr = title + '\n' + ingredients + '\n' + author + '\n' + prepTime + '\n' + \
           cookTime + '\n' + serving + '\n' + method + '\n' + dietary + '\n' + description
    aggr = unicodedata.normalize('NFKD', aggr).encode('ASCII', 'ignore')
    # print aggr
    return aggr


# Shingling function that shingle all documents by K characters and hash them.
def shingling(list_of_files, scraping_function, hashed=True):

    # Check whether the shingles set has been already built.
    if hashed:
        docShingleSets = load_binary_file(definitions.HASHED_SHINGLES_FILE)
    else:
        docShingleSets = load_binary_file(definitions.SHINGLES_FILE)

    if docShingleSets is not None:
        print 'Shingles loaded.'
        return docShingleSets

    print '\nShingling Documents...'

    # Create a dictionary of the documents, mapping the document identifier to the list of
    # shingle IDs that appear in the document.
    docShingleSets = dict()

    t0 = time.time()

    for filename in list_of_files:
        print filename
        # Read all the strings in the document.
        docstring = scraping_function(filename)

        docShingles = DocShingles(filename, docstring)

        # Store the completed list of shingles for this document in the dictionary.
        if hashed:
            docShingleSets[docShingles.docID] = docShingles.hash_shingles()
        else:
            docShingleSets[docShingles.docID] = docShingles.shinglesInDoc

    t1 = time.time()
    print 'Time to Shingling %d documents by %d characters: %f' % (len(list_of_files),
                                                                   SHINGLE_LENGTH,
                                                                   t1 - t0)
    # Store the shingles in a file for future uses, then return them.
    if not os.path.exists(definitions.FILE_DIR):
        os.makedirs(definitions.FILE_DIR)

    if hashed:
        save_binary_file(docShingleSets, definitions.HASHED_SHINGLES_FILE)
    else:
        save_binary_file(docShingleSets, definitions.SHINGLES_FILE)

    return docShingleSets


class DocShingles(object):
    # This class represents a Document and its shingles.
    def __init__(self, filename, docstring):
        """
        :param filename: paht of the document file.
        :param docstring: the document represented as a single string.
        """
        # Declare punctuation.
        exclude = set(string.punctuation)
        # Normalize text.
        st = re.sub(r'\s+', '', docstring)
        st = ''.join(ch for ch in st if ch not in exclude)
        # Shingles in the document.
        shingles_in_doc = {st[i:i + SHINGLE_LENGTH] for i in range(len(st) - SHINGLE_LENGTH + 1)}

        self.docID = filename
        self.shinglesInDoc = shingles_in_doc

    # Return hashed values of the shingles.
    def hash_shingles(self):
        hashed_shingles = set()
        for sh in self.shinglesInDoc:
            hashed_shingles.add(int(hashlib.md5(sh).hexdigest()[:16], 16))
            # hashed_shingles.add(binascii.crc32(sh) & 0xffffffff)
        return hashed_shingles
