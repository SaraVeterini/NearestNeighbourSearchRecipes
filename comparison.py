def compare():
    import os
    import definitions
    from shingling import scraping, shingling
    from minhash import DocMinHashSignatures
    from jaccard import Jaccard
    from lsh import Lsh


    files = os.listdir(definitions.RECIPES_FOLDER)
    shingles_map = shingling(files, scraping, hashed=True)
    jaccard_list = Jaccard(shingles_map).jaccardCandidates
    sign = DocMinHashSignatures(shingles_map)

    lsh_list = Lsh(sign).lsh_neighbours
    result = lsh_list.intersection(jaccard_list)
    file_result = open("result.txt", 'wb+')
    for item in result:
        file_result.write(str(item))