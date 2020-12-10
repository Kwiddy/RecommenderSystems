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
    stored_indices = []

    for index, row in comparison_df.iterrows():
        stored_indices.append(index)
        row = make_comparable(row)
        new_df.append(row)

    return cosine_similarity(new_df), stored_indices


def find_user_rated(user, rdf):
    user_reviews = rdf[rdf["user_id"] == user]
    return user_reviews


def find_neighbours(matrix, reviewed, business_index, return_num):
    id = reviewed["business_id"][0]
    for i in range(len(business_index)):
        if business_index[i] == id:
            row_loc = i
            break

    sims_id = []
    for i in range(len(matrix[row_loc])):
        sims_id.append([matrix[row_loc][i], business_index[i]])

    similarities = sorted(sims_id, reverse=True)

    # Remove self from list of similarities
    similarities = similarities[1:]

    return similarities[:return_num]


def display_results(results):
    output = pd.DataFrame()
    first = True
    for item in results:
        id = item[1]
        result = businesses_df[businesses_df["business_id"] == id]
        result["similarity"] = item[0]
        if first:
            output = result
            first = False
        else:
            output = pd.concat([output, result])
    print(output)


def test_funct():
    print("[A] 2U2tqOCphgOQ-NX8b3P6nw")
    print("[B] UHkDeBOmSKQCBIi9t8YzJw")
    print("[C] deB6EXuanGiN1tkSASuh3A")

    valid = False
    while not valid:
        choice = input("Input the letter corresponding to an ID: ")
        if choice.upper() == "A":
            chosen_id = "2U2tqOCphgOQ-NX8b3P6nw"
            valid = True
        elif choice.upper() == "B":
            chosen_id = "UHkDeBOmSKQCBIi9t8YzJw"
            valid = True
        elif choice.upper() == "C":
            chosen_id = "deB6EXuanGiN1tkSASuh3A"
            valid = True
        else:
            print("INVALID INPUT")
    return chosen_id


# Eventually this should be changeable, this is just for testing purposes
i_user_id = "2U2tqOCphgOQ-NX8b3P6nw"

i_user_id = test_funct()

# find the similarity matrix between all businesses and store locations for later use
similarity_matrix, indices = find_similarities(businesses_df)

# Find all businesses reviewed by the user
rated_items = find_user_rated(i_user_id, reviews_df)

# Find similar businesses to those which have been reviewed by user
neighbours = find_neighbours(similarity_matrix, rated_items, indices, 12)

display_results(neighbours)
