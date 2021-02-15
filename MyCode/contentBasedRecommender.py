# This recommender uses content-based filtering

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def content_based_recommender(reviewed_items, refined_businesses):
    similarity_measure = refined_businesses['categories']
    # TF-IDF algorithm, weights the importance of keywords based on frequency, higher weight = rarer and more important
    # TF = Term frequency, IDF = Inverse document frequency (relative significance)
    # Stop words are like "an" and "the" and hold no significant meaning so are removed
    # An n-gram range of 3-14 has been chosen so that all categories can be included within a single n-gram, for example
    #   both "pubs" and "sports bars"
    #
    # Calculate the relevance of one item to another
    # The following block of code (next 7 lines) have been adapted from:
    #   https://github.com/nikitaa30/Content-based-Recommender-System/blob/master/recommender_system.py
    tfidf_matrix = TfidfVectorizer(ngram_range=(1, 2), stop_words='english').fit_transform(similarity_measure)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    results = {}
    for index, row in refined_businesses.iterrows():
        similar_indices = cosine_similarities[index].argsort()[:-100:-1]
        similar_items = [[cosine_similarities[index][i], refined_businesses['business_id'][i]] for i in similar_indices]
        results[row['business_id']] = similar_items[1:]

    # Sum the similarities to all previously reviewed items to find most similar businesses to the user profile
    combined_results = []
    for business_id in reviewed_items:
        if len(combined_results) == 0:
            combined_results = results[business_id]
            print(combined_results)
        else:
            for result in results[business_id]:
                i = 0
                while i < len(combined_results):
                    if combined_results[i][1] == result[1]:
                        combined_results[i][0] += result[0]
                        break
                    i += 1

    # Sort the new list of combined results
    combined_results = sorted(combined_results, reverse=True)
    return combined_results
