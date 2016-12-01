import os
import definitions
from shingling import scraping, shingling


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
    files = ['applecharlotte_79046.html', 'applecharlotte_81084.html']
    map_shingles = shingling(files, scraping)
    for file1, list_of_file1 in map_shingles.iteritems():
        for file2, list_of_file2 in map_shingles.iteritems():
            if file1 < file2:
                print file1+" "+file2
                jac = Jaccard(list_of_file1, list_of_file2)
                print jac.jaccard
