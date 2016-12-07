import os

import definitions

from shingling import scraping, shingling
from minhash import DocMinHashSignatures
from jaccard import Jaccard
from lsh import Lsh


def compare():
    files = os.listdir(definitions.RECIPES_FOLDER)
    print len(files)
    # hashed_shingles_map = shingling(files, scraping, hashed=True)
    shingles_map = shingling(files, scraping, hashed=False)

    # compute jaccard similarity
    jaccard_list = Jaccard(shingles_map).jaccardNeighbours
    print len(jaccard_list)

    # compute minhashing and lsh
    sign = DocMinHashSignatures(shingles_map).minHashDocuments
    del shingles_map

    lsh_list = Lsh(sign).lshNeighbours
    print len(lsh_list)

    result = lsh_list.intersection(jaccard_list)

    file_result = open(definitions.COMP_RESULTS, 'w')
    for item in result:
        file_result.write(str(item))
    file_result.close()


if __name__ == '__main__':
    compare()
