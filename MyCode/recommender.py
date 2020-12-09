# 2 personalised recommender systems
# cli
# 1 must be collaborative: collaborative content-based, collaborative demographic, collaborative knowledge-based
# choose the hybrid scheme: weighted, mixed, switching, feature combination, feature augmentation, cascade
#
# collaborative should be item-item?
# look at paper in wk 4 movie recommender
#
# Measure the similarity between users to find neighbours. e.g. pearson correlation
# use regression / classification -- I would need to do regression? because ordering matters i.e. its a continuous scale

import pandas as pd
import sklearn
import numpy as np
import math
import scipy
from sklearn.metrics.pairwise import cosine_similarity

businesses = pd.read_csv("newDFBusiness.csv")
reviews = pd.read_csv("newDFReview.csv")
users = pd.read_csv("newDFUser.csv")
# print(reviews)

# relevant duo link:
# https://duo.dur.ac.uk/bbcswebdav/pid-6063283-dt-content-rid-21459602_2/courses/COMP3607_2020/W4%20-%20Collaborative%20filtering%20-%20part%201%281%29.pdf


def remove_zeros(user, neighbour):
    cleansed_user = []
    cleansed_neighbour = []
    for i in range(len(user)):
        if user[i] != 0 and neighbour[i] != 0:
            cleansed_user.append(user[i])
            cleansed_neighbour.append(neighbour[i])
    return np.array(cleansed_user, dtype="int64"), np.array(cleansed_neighbour, dtype="int64")


def make_comparable(items_row):
    comparable = []
    for item in items_row:
        if type(item) in [float, int]:
            comparable.append(item)
    comparable = comparable[1:]
    # return np.array(comparable)
    return comparable


def find_neighbours(comparison_df):# target_user):
    comparison_df = comparison_df.set_index("business_id")
    neighbours = []
    new_df = []

    # print(comparison_df)
    for index, row in comparison_df.iterrows():
        row = make_comparable(row)
        new_df.append(row)
        print(row)

    # print(cosine_similarity(comparison_df))

    # for index, row in comparison_df.iterrows():
    #     if index == target_user:
    #         user_row = row.to_numpy()
    #         user_comparison = make_comparable(user_row)
    #         break
    #
    # for index, row in comparison_df.iterrows():
    #     if index != target_user:
    #         row = row.to_numpy()
    #         neighbour_comparison = make_comparable(row)
    #         t_user_comparison, t_neighbour_comparison = remove_zeros(user_comparison, neighbour_comparison)
    #         similarity = 1 - scipy.spatial.distance.cosine(t_user_comparison, t_neighbour_comparison)
    #         neighbours.append([index, similarity])

    return sorted(neighbours, key=lambda x: x[1], reverse=True)


# Eventually this should be changeable, this is just for testing purposes
i_user_id = "2U2tqOCphgOQ-NX8b3P6nw"
# sorted_neighbours = find_neighbours(users, i_user_id)
sorted_neighbours = find_neighbours(businesses)

# print(sorted_neighbours)

