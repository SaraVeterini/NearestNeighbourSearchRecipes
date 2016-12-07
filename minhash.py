# ===== Generate MinHash Signatures ===== #
import os
import time
import struct
import hashlib

import definitions

from utils.loader import save_binary_file, load_binary_file

N = 10


def hash_family(n):
    resultSize = 8
    maxLen = 20
    salt = str(n).zfill(maxLen)[-maxLen:]

    def hashMember(x):
        return int(hashlib.sha1(x + salt).hexdigest()[-resultSize:], 16)

    return hashMember


class DocMinHashSignatures(object):
    def __init__(self, dictionary_of_set, numHashes=N):
        print '\nGenerating MinHash signatures for all documents...'

        # Check whether the signatures have been already computed.
        signatures = load_binary_file(definitions.SIGNATURES_FILE)

        if signatures is not None:
            self.minHashDocuments = signatures
            print 'MinHash signatures loaded.'

        else:
            # List of docs represented as signature vectors
            signatures = dict()

            t0 = time.time()
            # For each document...
            for docID in dictionary_of_set.keys():

                # Get the shingle set for this document.
                shingleSet = dictionary_of_set[docID]

                # The resulting minhash signature for this document.
                signature = list()

                # For each hash function...
                for i in range(0, numHashes):

                    # For each of the shingles actually in the document, calculate its hash code
                    # using hash function 'i'.
                    hash_function = hash_family(i)

                    # Initialize 'minHashCode' to positive infinity.
                    minHashCode = float('inf')

                    # For each shingle in the document...
                    for shingle in shingleSet:
                        # Evaluate the hash function.
                        hashCode = hash_function(shingle)

                        # Record the lowest hash code.
                        if hashCode < minHashCode:
                            minHashCode = hashCode

                    # Add the smallest hash code value as component number 'i' of the signature.
                    signature.append(minHashCode)

                # Store the MinHash signature for this document.
                signatures[docID] = signature

            elapsed = time.time() - t0

            print 'Generated %d signatures for %d documents in %f seconds' \
                  % (numHashes, len(dictionary_of_set.keys()), elapsed)

            # Store signatures in a file for future uses.
            if not os.path.exists(definitions.FILE_DIR):
                os.makedirs(definitions.FILE_DIR)
            save_binary_file(signatures, definitions.SIGNATURES_FILE)

            self.minHashDocuments = signatures
