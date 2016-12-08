import time

import definitions

from utils.loader import save_binary_file, load_binary_file


class Jaccard(object):
    def __init__(self, shingles_map):
        """
        implement a class that given the shingles of each of the documents, finds the
        nearest neighbors by comparing all the shingle sets with each other, using
        the Jaccard similarity.

        :param shingles_map: dictionary of shingles.
        """
        print '\nComputing Jaccard Similarity...'

        # Check whether the jaccard similarity have been already computed.
        jaccard = load_binary_file(definitions.JACCARD_FILE)

        if jaccard is not None:
            self.jaccardNeighbours = jaccard
            print 'Jaccard similarity file loaded.'

        else:
            file_result_jaccard = open(definitions.JACCARD_RESULTS, 'w')
            t0 = time.time()
            neigh = []

            for key1, set1 in shingles_map.iteritems():
                for key2, set2 in shingles_map.iteritems():
                    if key2 > key1:
                        n = len(set1.intersection(set2))
                        sim = n / float(len(set1) + len(set2) - n)
                        if sim >= 0.8:
                            neigh.append((key1, key2))
                            file_result_jaccard.write(str((key1, key2)) + '\n')

            elapsed = time.time() - t0
            file_result_jaccard.close()
            print 'Jaccard similarity of %d documents computed in %f seconds' \
                  % (len(shingles_map.keys()), elapsed)

            save_binary_file(neigh, definitions.JACCARD_FILE)
            self.jaccardNeighbours = neigh
