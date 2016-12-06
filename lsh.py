
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


def compute_hash(vector):
    return hash(str(vector))


class Lsh(object):
    def __init__(self, minhash_map):
        candidates_list = list()
        for doc_id1, minhash_list1 in minhash_map.iteritems():
            for doc_id2, minhash_list2 in minhash_map.iteritems():
                if doc_id2 > doc_id1:
                    # iterate over bands
                    for i in range(0, B):
                        # calculate hashes for each document
                        hash_doc1 = compute_hash(minhash_list1[i*R:(i+1)*R])
                        hash_doc2 = compute_hash(minhash_list2[i*R:(i+1)*R])
                        # 2 documents are candidates if their subvector is the same in at least one band
                        if hash_doc1 == hash_doc2:
                            candidates_list.append((doc_id1, doc_id2))
                            break

        print "Candidates list: "+str(candidates_list)

        self.lshCandidates = candidates_list


if __name__ == '__main__':
    import os
    import definitions
    import shingling
    import minhash

    files = os.listdir(definitions.RECIPES_FOLDER)
    dictionary_of_shingles = shingling.shingling(files[2000:4000], shingling.scraping, hashed=True)
    map_minhash = minhash.DocMinHashSignatures(dictionary_of_shingles, 100).minHashDocuments
    Lsh(map_minhash)
