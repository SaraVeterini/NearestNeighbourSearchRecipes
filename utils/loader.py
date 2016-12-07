try:
    import cPickle as pickle
except:
    import pickle


def save_binary_file(obj, filename):
    """
    Save an inverted index in a binary file
    :param inverted_index:  an instance of 'invertedindex'
    :return:                boolean (success or error)
    """
    with open(filename, 'wb') as f:
        try:
            pickle.dump(obj, f, -1)
            return True
        except pickle.PickleError:
            return False


def load_binary_file(filename):
    """
    Load an inverted index from a binary file
    :return: an instance of 'invertedindex'
    """
    try:
        with open(filename, 'rb') as f:
            try:
                d = pickle.load(f)
            except pickle.PickleError:
                d = None
    except IOError:
        print "%s not found" % str(filename)
        d = None
    return d
