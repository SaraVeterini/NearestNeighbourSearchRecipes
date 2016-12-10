import os

import definitions

from shingling import scraping, shingling
from minhash import DocMinHashSignatures, N
from jaccard import Jaccard
from lsh import Lsh, B, R


def intersect_lists(list1, list2):
    res = []
    for e1 in list1:
        for e2 in list2:
            if e1 == e2:
                res.append(e1)
    return res


def compare(lsh_iterations):
    files = os.listdir(definitions.RECIPES_FOLDER)
    print '\nNumber of Documents: %d' % len(files)

    # compute shingling.
    shingles_map = shingling(files, scraping, hashed=True)

    # compute jaccard similarity.
    jaccard_list = Jaccard(shingles_map).jaccardNeighbours

    # compute minhashing and lsh.
    lsh_length = []
    intersections = []
    false_positives = []
    print '\nNumber of Hash function used with LSH: %d' % N
    print 'Band parameter B: %d' % B
    print 'Rows parameter R: %d' % R
    print 'Running %d iterations of MinHash - LSH ...' % lsh_iterations
    for i in range(lsh_iterations):
        print '\n#' + ('='*30) + '#'
        print 'Iteration #%d' % (i + 1)
        # compute signatures
        signatures = DocMinHashSignatures(shingles_map, saveFile=False).minHashDocuments
        # compute LSH
        lsh_list = Lsh(signatures).lshNeighbours
        # check the intersection between the Jaccard results and the current LSH iteration
        intersection = intersect_lists(jaccard_list, lsh_list)

        lsh_length.append(len(lsh_list))
        intersections.append(len(intersection))
        false_positives.append(max(len(lsh_list) - len(intersection), 0))

    ml = (float(sum(lsh_length)) / float(lsh_iterations))
    fp = (float(sum(false_positives)) / float(lsh_iterations))

    ma = (float(sum(intersections)) / float(lsh_iterations))
    jl = float(len(jaccard_list))

    print '\n#' + ('=' * 16) + '#'
    print '\nLSH Mean false-positives: %f' % (fp / ml)

    print '\nLSH Mean accuracy in LSH: %f' % (ma / jl)


if __name__ == '__main__':
    compare(5)
