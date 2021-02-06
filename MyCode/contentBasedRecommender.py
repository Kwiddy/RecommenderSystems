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

ds = pd.read_csv("newDFBusiness.csv")

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['categories'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [[cosine_similarities[idx][i], ds['business_id'][i]] for i in similar_indices]

    results[row['business_id']] = similar_items[1:]

print(results)