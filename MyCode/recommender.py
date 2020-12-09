import pandas as pd
import sklearn
import numpy as np
import math
import scipy
from sklearn.metrics.pairwise import cosine_similarity

businesses_df = pd.read_csv("newDFBusiness.csv")
reviews_df = pd.read_csv("newDFReview.csv")
users_df = pd.read_csv("newDFUser.csv")


def make_comparable(items_row):
    comparable = []
    for item in items_row:
        if type(item) in [float, int] and not math.isnan(item):
            comparable.append(item)
    return comparable[1:]


def find_similarities(comparison_df):
    comparison_df = comparison_df.set_index("business_id")
    new_df = []

    for index, row in comparison_df.iterrows():
        row = make_comparable(row)
        new_df.append(row)

    return cosine_similarity(new_df)


def find_user_rated(user, rdf, bdf):
    user_reviews = rdf[rdf["user_id"] == user]
    return user_reviews


# Eventually this should be changeable, this is just for testing purposes
i_user_id = "2U2tqOCphgOQ-NX8b3P6nw"

similarity_matrix = find_similarities(businesses_df)
print(similarity_matrix)

rated_items = find_user_rated(i_user_id, reviews_df, businesses_df)
print(rated_items)

