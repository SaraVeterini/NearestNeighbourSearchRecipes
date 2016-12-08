import os
import math

import numpy as np
import matplotlib.pyplot as plt

import definitions

from utils.loader import save_binary_file, load_binary_file
from shingling import scraping, shingling
from minhash import DocMinHashSignatures
from jaccard import Jaccard
from lsh import Lsh


def plot_results(jaccard, lsh):
    ag = []
    for e in jaccard:
        ag.append(e[0])
    for e in jaccard:
        ag.append(e[1])
    for e in lsh:
        ag.append(e[0])
    for e in lsh:
        ag.append(e[1])

    uniques, Z = np.unique(ag, return_inverse=True)
    xj = Z[:len(jaccard)]
    yj = Z[len(jaccard):len(jaccard) * 2]
    xl = Z[len(jaccard) * 2:(len(jaccard) * 2) + len(lsh)]
    yl = Z[(len(jaccard) * 2) + len(lsh):len(Z)]

    fig = plt.figure(111)
    size = max(math.fabs(len(xl) - len(xj)) ** 2, 25)
    plt.scatter(xj, yj, c='red', alpha=.5, s=size, label='Jaccard')
    plt.scatter(xl, yl, c='blue', alpha=.4, s=size, label='LSH')
    plt.xlim((-0.5, max(max(xj), max(xl)) + 1))
    plt.ylim((-0.5, max(max(yj), max(yl)) + 1))
    plt.legend()
    plt.show()


def intersect_lists(list1, list2):
    res = []
    for e1 in list1:
        for e2 in list2:
            if e1 == e2:
                res.append(e1)
    return res


def compare(lsh_iterations):
    files = os.listdir(definitions.RECIPES_FOLDER)
    print 'Number of Documents: %d' % len(files)

    # compute shingling.
    shingles_map = shingling(files, scraping, hashed=False)

    # compute jaccard similarity.
    jaccard_list = Jaccard(shingles_map).jaccardNeighbours

    # compute minhashing and lsh.
    lsh_length = []
    intersections = []
    false_positives = []
    for i in range(lsh_iterations):
        signatures = DocMinHashSignatures(shingles_map, saveFile=False).minHashDocuments
        lsh_list = Lsh(signatures).lshNeighbours
        intersection = intersect_lists(jaccard_list, lsh_list)
        lsh_length.append(len(lsh_list))
        intersections.append(len(intersection))
        false_positives.append(len(lsh_list) - len(intersection))

    ml = (float(sum(lsh_length)) / float(lsh_iterations))
    fp = (float(sum(false_positives)) / float(lsh_iterations))
    ma = (float(sum(intersections)) / float(lsh_iterations))

    print '\nLSH Mean false-positives: %f' % (fp / ml)

    print '\nLSH Mean accuracy in LSH: %f' % (ma / ml)

    print '\nEnd'


if __name__ == '__main__':
    compare(2)
