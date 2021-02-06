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

businesses_df = pd.read_csv("newDFBusiness.csv")

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(businesses_df['categories'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}

for index, row in businesses_df.iterrows():
    similar_indices = cosine_similarities[index].argsort()[:-100:-1]
    similar_items = [[cosine_similarities[index][i], businesses_df['business_id'][i]] for i in similar_indices]

    results[row['business_id']] = similar_items[1:]

print(results)


def item(id):
    return businesses_df.loc[businesses_df['business_id'] == id]['business_id'].tolist()[0].split(' - ')[0]

def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")
    print("-------")
    recs = results[item_id][:num]
    for rec in recs:
        print("Recommended: " + item(rec[1]) + " (score:" + str(rec[0]) + ")")


recommend(item_id="ZpPOiNYi4AHNneI7uco7GQ", num=5)