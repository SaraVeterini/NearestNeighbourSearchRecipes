def compute_jaccard_index(set_1, set_2):
    n = len(set_1.intersection(set_2))
    return n / float(len(set_1) + len(set_2) - n)


class Jaccard(object):
    def __init__(self, shinglesFirstSet, shinglesSecondSet):
        """
            :param shinglesFirstSet: shingles of first set.
            :param shinglesSecondSet: shingles of second set.
        """
        self.jaccard = compute_jaccard_index(shinglesFirstSet, shinglesSecondSet)

if __name__ == '__main__':
    jac = Jaccard(set([0, 1, 2, 3]), set([0, 2, 3, 4]))
    print jac.jaccard