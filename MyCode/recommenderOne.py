# This is a neighbourhood-based collaborative filtering method (item-based)

# imports
import math
import pandas as pd
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity


def recommender_one(user_id):

    # Update the dataframes
    reviews_df = pd.read_csv("newDFReview.csv")
    users_df = pd.read_csv("newDFUser.csv")
    businesses_df = pd.read_csv("newDFBusiness.csv")

    # find the similarity matrix between all businesses and store locations for later use
    similarity_matrix, indices = find_similarities(businesses_df)

    # Find all businesses reviewed by the user
    rated_items = find_user_rated(user_id, reviews_df)

    # Find blacklisted items
    id_search = users_df[users_df["user_id"] == user_id]
    blacklist_str = id_search['blacklist'].iloc[0]
    blacklist = []
    if not pd.isna(blacklist_str):
        blacklist = blacklist_str.split(",")

    # Find the predictions for each item and find the items to be recommended
    weighted_average = find_predictions(similarity_matrix, user_id, rated_items, indices, businesses_df, users_df,
                                        reviews_df, blacklist)

    # Return recommender predictions
    return weighted_average


# Find the similarity matrix between businesses
def find_similarities(comparison_df):
    comparison_df = comparison_df.set_index("business_id")
    new_df = []
    stored_indices = []

    # Store indices of each row
    for index, row in comparison_df.iterrows():
        stored_indices.append(index)

        # Refine the data in each row so that it can be compared
        row = make_comparable(row)

        # Add the new row to the new dataframe
        new_df.append(row)

    # Return the cosine similarities of the new dataframe along with the stored indices
    return cosine_similarity(new_df), stored_indices


# Find the businesses in the refined dataset which the user has rated
def find_user_rated(user, rdf):
    user_reviews = rdf[rdf["user_id"] == user]
    return user_reviews


# Make a row from the businesses dataframe comparable
def make_comparable(items_row):
    comparable = []

    # remove any cell which is not a numeric type
    for item in items_row:
        if type(item) in [float, int] and not math.isnan(item):
            comparable.append(item)
    return comparable[1:]


# Calculate predictions for each item and find the items to be recommended
def find_predictions(matrix, user, rated, business_index, businesses_df, users_df, reviews_df, blacklist):
    # Find the location of the reviewed items in the similarity matrix
    n_final_similarities = []
    d_final_similarities = []
    reviewed_stars = []
    for item in rated["business_id"]:

        reviewed_id = item
        rated_item = rated.loc[rated["business_id"] == reviewed_id]
        reviewed_stars.append(int(rated_item["stars"]))

        for i in range(len(business_index)):
            if business_index[i] == reviewed_id:
                row_loc = i
                break

        # Find all items (to predict) which have a similarity to the reviewed item
        sims_id = []
        for i in range(len(matrix[row_loc])):
            if i != row_loc:
                sims_id.append([matrix[row_loc][i], business_index[i]])

        # Append similarities to a list of all similarity scores for each reviewed item
        n_final_similarities.append(sims_id)
        d_final_similarities.append(sims_id)

    # reviewed_item = item in reviewed
    # reviewed_stars = user rating
    # (n|d)_final_similarities = matrix of matrices of similarities for items being predicted

    temp = []
    for i in range(len(n_final_similarities)):
        multiplier = reviewed_stars[i]
        temp2 = []
        for j in range(len(n_final_similarities[i])):
            product = multiplier * n_final_similarities[i][j][0]
            new_item = [product, n_final_similarities[i][j][1]]
            temp2.append(new_item)
        temp.append(temp2)
    n_final_similarities = temp

    # numerator:
    # SUM(multiply user's rating by the similarity score between item being predicted and each item in reviewed)
    numerators = []

    for j in range(len(n_final_similarities[0])):
        sum_total = 0
        predict_id = n_final_similarities[0][j][1]
        for i in range(len(n_final_similarities)):
            sum_total += n_final_similarities[i][j][0]
        numerators.append([sum_total, predict_id])

    # denominator:
    # SUM(ABS(each similarity between the item being predicted and each item in reviewed))
    denominators = []

    for j in range(len(d_final_similarities[0])):
        sum_total = 0
        predict_id = d_final_similarities[0][j][1]
        for i in range(len(d_final_similarities)):
            sum_total += abs(d_final_similarities[i][j][0])
        denominators.append([sum_total, predict_id])

    # Create the predictions for each item by dividing the numerator elements by the corresponding denominator elements
    predictions = []
    for i in range(len(numerators)):
        n = numerators[i][0]
        d = denominators[i][0]
        result = n/d
        predictions.append([result, numerators[i][1]])

    # Sort the predictions
    sorted_predictions = sorted(predictions, reverse=True)

    # remove blacklisted items
    for item in sorted_predictions:
        if item[1] in blacklist:
            sorted_predictions.remove(item)

    # remove items with a below minimum number of stars (from preferences)
    id_search = users_df[users_df["user_id"] == user]
    min_stars = id_search['min_stars'].iloc[0]
    for item in sorted_predictions:
        business_search = businesses_df[businesses_df["business_id"] == item[1]]
        num_stars = business_search['stars'].iloc[0]
        num_stars = int(num_stars)
        if num_stars < int(min_stars):
            sorted_predictions.remove(item)

    # If the user has chosen not to recommend previously reviewed items then remove them from the predictions
    prev_seen_pref = id_search['recommend_seen'].iloc[0]
    to_remove = []
    if prev_seen_pref == "N":
        user_reviews = reviews_df[reviews_df["user_id"] == user]
        for index, row in user_reviews.iterrows():
            to_remove.append(row["business_id"])
        for item in sorted_predictions:
            if item[1] in to_remove:
                sorted_predictions.remove(item)

    # Remove items based on the user's advanced preferences
    advanced_preferences = id_search['advanced_preferences'].iloc[0]
    advanced_preferences = literal_eval(advanced_preferences)
    for item in sorted_predictions:
        business_search = businesses_df[businesses_df["business_id"] == item[1]]
        attributes = business_search['attributes'].iloc[0]

        # Leave the businesses with nan values as their attributes
        try:
            if math.isnan(attributes):
                pass
        except:
            # Check if each preference is in the business' attributes and if so, make sure it matches otherwise remove
            attributes = literal_eval(attributes)
            for preference in advanced_preferences:
                if preference in attributes:
                    if attributes[preference] != advanced_preferences[preference]:
                        sorted_predictions.remove(item)
                        break

    # Return the list of sorted predictions
    return sorted_predictions
