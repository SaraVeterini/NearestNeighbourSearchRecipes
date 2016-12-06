import time


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
        t0 = time.time()
        cand = []
        for key1 in shingles_map:
            for key2 in shingles_map:
                if key2 > key1:
                    sim = compute_jaccard_index(shingles_map[key1], shingles_map[key2])
                    if sim >= 0.8:
                        cand.append((key1, key2))
        elapsed = time.time() - t0
        print 'Jaccard similarity of %d documents computed in %f' % (len(shingles_map.keys()), elapsed)
        self.jaccardCandidates = cand


if __name__ == '__main__':
    import os
    import definitions
    from shingling import scraping, shingling

    files = os.listdir(definitions.RECIPES_FOLDER)
    files = sorted(files)
    shingles_map = shingling(files[:1000], scraping, hashed=False)
    cand = Jaccard(shingles_map).jaccardCandidates
    print cand
    print len(cand)
