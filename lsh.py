import time

import definitions

''' B is the number of bands
    R is the number of rows in each band.
    if N is the number of hash functions for calculating minhash,
    it must be

    B*R = N
    (1/B)^(1/R)> 0.8

    where 0.8 is the threshold, the value of the jaccard similarity
    above which the probability that 2 documents are chosen as candidates to be
    similar is 1/2 '''
B = 2
R = 5


class Lsh(object):
    def __init__(self, minhash_map):
        print '\nComputing LSH...'
        candidates_list = list()

        t0 = time.time()
        for doc_id1, minhash_list1 in minhash_map.iteritems():
            for doc_id2, minhash_list2 in minhash_map.iteritems():
                if doc_id2 > doc_id1:
                    # iterate over bands
                    for i in range(0, B):
                        # calculate hashes for each document
                        hash_doc1 = hash(str(minhash_list1[i*R:(i+1)*R]))
                        hash_doc2 = hash(str(minhash_list2[i*R:(i+1)*R]))
                        # 2 documents are candidates if their subvector is the same in at least one band
                        if hash_doc1 == hash_doc2:
                            candidates_list.append((doc_id1, doc_id2))
                            break

        t1 = time.time() - t0
        print 'Time to compute LSH candidates: %f seconds' % t1
        self.lshCandidates = candidates_list

        file_result_lsh = open(definitions.LSH_RESULTS, 'w')
        estimate_jaccard_list = list()
        counter = 0

        for (doc_1, doc_2) in candidates_list:
            for i in range(len(minhash_list1)):
                if minhash_map[doc_1][i] == minhash_map[doc_2][i]:
                    counter += 1
            if counter/len(minhash_list1) >= 0.8:
                estimate_jaccard_list.append((doc_1, doc_2))
                file_result_lsh.write(str((doc_1, doc_2)) + '\n')

        t2 = time.time() - t0
        file_result_lsh.close()
        print 'Time to compute LSH neighbours: %f seconds' % t2
        self.lshNeighbours = estimate_jaccard_list
