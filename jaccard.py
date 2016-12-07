import time

import definitions


def compute_jaccard_index(set_1, set_2):
    n = len(set_1.intersection(set_2))
    return n / float(len(set_1) + len(set_2) - n)


class Jaccard(object):
    def __init__(self, shingles_map):
        """
        implement a class that given the shingles of each of the documents, finds the
        nearest neighbors by comparing all the shingle sets with each other, using
        the Jaccard similarity.

        :param shingles_map: dictionary of shingles.
        """
        print '\nComputing Jaccard Similarity...'
        file_result_jaccard = open(definitions.JACCARD_RESULTS, 'w')
        t0 = time.time()
        neigh = []

        for key1 in shingles_map:
            for key2 in shingles_map:
                if key2 > key1:
                    sim = compute_jaccard_index(shingles_map[key1], shingles_map[key2])
                    if sim >= 0.8:
                        neigh.append((key1, key2))
                        file_result_jaccard.write(str((key1, key2)))

        file_result_jaccard.close()
        elapsed = time.time() - t0
        print 'Jaccard similarity of %d documents computed in %f seconds' % (len(shingles_map.keys()), elapsed)
        self.jaccardNeighbours = neigh
