import pandas as pd
import sklearn
import numpy as np
import math
import scipy
from sklearn.metrics.pairwise import cosine_similarity


def select_user(user_df):
    input_own_choice = input("Please enter [N] for inputting a chosen user id, or [S] to select from pre-chosen IDs: ")

    if input_own_choice.upper() == "S":
        print("[A] 2U2tqOCphgOQ-NX8b3P6nw")
        print("[B] UHkDeBOmSKQCBIi9t8YzJw")
        print("[C] deB6EXuanGiN1tkSASuh3A")
        print("[X] - Exit")

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
            elif choice.upper() == "X":
                exit()
            else:
                print("INVALID INPUT")
        print()
        return chosen_id

    elif input_own_choice.upper() == "N":
        valid_input = False
        while not valid_input:
            chosen_id = input("Please enter user ID (or enter [S] to return / [X] to exit): ")
            if chosen_id.upper() == "S":
                valid_input = True
                chosen_id = select_user(user_df)
            elif chosen_id.upper == "X":
                exit()
            else:
                user_reviews = user_df[user_df["user_id"] == chosen_id]
                if len(user_reviews) > 0:
                    valid_input = True
                else:
                    print("INVALID INPUT - Sorry, it looks like we don't have any users with this ID")
        print()
        return chosen_id


def display_results(results):
    output = pd.DataFrame()
    first = True
    for item in results:
        item_id = item[1]
        result = businesses_df.loc[businesses_df["business_id"] == item_id].copy()
        result["Prediction"] = item[0]
        if first:
            output = result
            first = False
        else:
            output = pd.concat([output, result])
    print(output)


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


def anything_else(user_id):
    print("Please choose one of the options below: ")
    print("[M] - Continue")
    print("[L] - Logout and enter another user ID")
    print("[X] - Close the program")
    valid = False
    while not valid:
        choice = input("Choice: ")

        if choice.upper() == "X":
            valid = True
            exit()
        elif choice.upper() == "L":
            valid = True
            print()
            main(True, user_id)
        elif choice.upper() == "M":
            valid = True
            print()
            main(False, user_id)
        elif choice.upper() == "EXIT":
            exit()
        else:
            print("INVALID CHOICE")
    print()



def find_predictions(matrix, user, rated, business_index, return_num):
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
    sorted_predictions = sorted_predictions[:return_num]

    return sorted_predictions


def generate_recommendations(user_id):
    # find the similarity matrix between all businesses and store locations for later use
    similarity_matrix, indices = find_similarities(businesses_df)

    # Find all businesses reviewed by the user
    rated_items = find_user_rated(user_id, reviews_df)

    # Find the predictions for each item and find the items to be recommended
    weighted_average = find_predictions(similarity_matrix, user_id, rated_items, indices, 12)

    display_results(weighted_average)


def main(new_user, existing_user):
    if new_user:
        i_user_id = select_user(users_df)
    else:
        i_user_id = existing_user

    # Allow user to choose their service
    print("[R] - Generate list of recommendations")
    print("[N] - Add a new review")
    print("[E] - Update an existing review")
    print("[P] - Update user preferences")
    print("[X] - Exit")

    valid_choice = False
    while not valid_choice:
        choice = input("Please choose from the services listed above: ")

        if choice.upper() == "R":
            valid_choice = True
            print()
            generate_recommendations(i_user_id)
        elif choice.upper() == "X":
            exit()
        else:
            print("INVALID CHOICE - Please select from the list provided")

    anything_else(i_user_id)


businesses_df = pd.read_csv("newDFBusiness.csv")
reviews_df = pd.read_csv("newDFReview.csv")
users_df = pd.read_csv("newDFUser.csv")

main(True, "")