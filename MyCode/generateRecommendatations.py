import math
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def generate_recommendations(user_id, businesses_df, reviews_df, users_df):
    # find the similarity matrix between all businesses and store locations for later use
    similarity_matrix, indices = find_similarities(businesses_df)

    # Find all businesses reviewed by the user
    rated_items = find_user_rated(user_id, reviews_df)

    # Find the predictions for each item and find the items to be recommended
    weighted_average = find_predictions(similarity_matrix, user_id, rated_items, indices)

    #   To display is the users preference for the number of results to show
    id_search = users_df[users_df["user_id"] == user_id]
    to_display = id_search['display_num'].iloc[0]
    display_results(weighted_average, businesses_df, to_display)


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


def make_comparable(items_row):
    comparable = []
    for item in items_row:
        if type(item) in [float, int] and not math.isnan(item):
            comparable.append(item)
    return comparable[1:]


def find_predictions(matrix, user, rated, business_index):
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

    # numerator = SUM(multiply user's rating by the similarity score between item being predicted and each item in reviewed)
    numerators = []

    for j in range(len(n_final_similarities[0])):
        sum_total = 0
        predict_id = n_final_similarities[0][j][1]
        for i in range(len(n_final_similarities)):
            sum_total += n_final_similarities[i][j][0]
        numerators.append([sum_total, predict_id])

    # denominator = SUM(ABS(each similarity between the item being predicted and each item in reviewed))
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

    # Only return the top n predictions
    sorted_predictions = sorted_predictions

    return sorted_predictions


def display_results(results, businesses_df, return_num):
    show_more = True
    start = 0
    while show_more:
        output = pd.DataFrame()
        first = True
        for item in results[start:return_num]:
            last_row = item
            item_id = item[1]
            result = businesses_df.loc[businesses_df["business_id"] == item_id].copy()
            result["Prediction"] = item[0]
            if first:
                output = result
                first = False
            else:
                output = pd.concat([output, result])
        print(output)

        # Ensures that the user can only keep displaying more recommendations up until the end of the recommendations
        #       generated.
        if last_row != results[-1]:
            valid_choice = False
            while not valid_choice:
                yn = input("Display 10 more recommendations? [Y/N]: ")
                if yn.upper() == "Y":
                    valid_choice = True
                    start += 10
                    return_num += 10
                elif yn.upper() == "N":
                    valid_choice = True
                    show_more = False
                else:
                    print("INVALID INPUT")
        else:
            show_more = False
    print()