# # This recommender uses content-based filtering
#
# # imports
# import pandas as pd
#
#
# def content_based_recommender(user_id):
#     # Update the dataframes
#     reviews_df = pd.read_csv("newDFReview.csv")
#     users_df = pd.read_csv("newDFUser.csv")
#     businesses_df = pd.read_csv("newDFBusiness.csv")
#
#     return temporary_recommender(businesses_df)
#
#
# def temporary_recommender(businesses_df):
#     rank = 1
#     temp_rankings = []
#     for index, row in businesses_df.iterrows():
#         temp_rankings.append([rank, row["business_id"]])
#         rank += 1
#     temp_rankings = sorted(temp_rankings, reverse=True)
#     return temp_rankings












######################################################################################################################





# Ideas: At the moment takes a business id and returns a list of predictions (based only on categories which is poor)
# What about: It sums the combined predictions for businesses the user has already reviewed?  And then orders the
# Matching businesses from the cascade accordingly


# Base code from:
#   https://github.com/nikitaa30/Content-based-Recommender-System/blob/master/recommender_system.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def content_based_recommender(reviewed_items, refined_businesses):

    # TF-IDF algorithm, weights the importance of keywords based on frequency, higher weight = rarer and more important
    # TF = Term frequency, IDF = Inverse document frequency (relative significance)
    # Stop words are like "an" and "the" and hold no significant meaning so are removed
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(refined_businesses['categories'])

    # Calculate the relevance of one item to another
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
    print(combined_results)
    exit()

