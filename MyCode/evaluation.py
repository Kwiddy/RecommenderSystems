# imports
import pandas as pd
import math
from hybridRecommender import *

# stop copying error from appearing
pd.options.mode.chained_assignment = None  # default='warn'


# Find the metrics of the system
def find_metrics(users_df, reviews_df):

    user_review_limit = 3

    # Known size of the test set
    total_known = 0

    # Find the test users for evaluation (they must have enough unique reviews)
    test_users = []
    for index, row in users_df.iterrows():
        u_id = row["user_id"]
        id_search = reviews_df[reviews_df["user_id"] == u_id]
        seen = []
        count = 0
        for i, r in id_search.iterrows():
            if r["business_id"] not in seen:
                seen.append(r["business_id"])
                count += 1
        if count > user_review_limit:
            test_users.append(u_id)
            total_known += count

    # List of lists, item 1 = predicted score and item 0 = actual score
    ratings_comparison_h = []
    ratings_comparison_b = []
    ratings_comparison_c = []

    # True positive, False Negative, False Positive, True Negative    counters
    tp_h = 0
    fn_h = 0
    fp_h = 0
    tn_h = 0
    tp_b = 0
    fn_b = 0
    fp_b = 0
    tn_b = 0
    tp_c = 0
    fn_c = 0
    fp_c = 0
    tn_c = 0

    # Explainability trackers
    total_explained = 0
    total_recommended = 0

    # So only compute novelty once
    novelty_done = False

    # For each user
    for user in test_users:
        # Take all reviewed_id's and remove them one at a time
        # Generate Content-Based recommendations using previous reviews
        reviewed_ids = []
        user_reviews = reviews_df[reviews_df["user_id"] == user]
        for index, row in user_reviews.iterrows():
            reviewed_ids.append(row["business_id"])

        # Remove duplicate IDs
        reviewed_ids = list(dict.fromkeys(reviewed_ids))

        rated = reviews_df[reviews_df["user_id"] == user]
        # replace multiple reviews for a single business with one average review
        # print(rated)
        seen = []
        to_keep = []
        for index, row in rated.iterrows():
            if row["business_id"] not in seen:
                seen.append(row["business_id"])
                to_keep.append(row["review_id"])
                id_search = rated[rated["business_id"] == row["business_id"]]

                # If a business has been rated multiple times
                if len(id_search) != 1:
                    avg_list = []
                    for i, r in id_search.iterrows():
                        avg_list.append(int(r["stars"]))
                    avg = int(round(sum(avg_list) / len(avg_list), 0))
                    rated.loc[index, "stars"] = avg

        # Remove any reviews not in to_keep
        rated = rated[rated.review_id.isin(to_keep)]

        ### Novelty Calculation
        first_recommendations, refined_businesses, explanatory_refs = collaborative_recommender(user)

        copy = []
        for item in first_recommendations:
            copy.append(item)

        second_recommendations = content_based_recommender(reviewed_ids, refined_businesses, user)

        # Apply a cascade scheme to join the two recommender systems
        final_recommendations = cascade_scheme(first_recommendations, second_recommendations)
        total_explained += len(explanatory_refs)
        total_recommended += len(final_recommendations)

        i = 0
        while i < len(reviewed_ids):
            temp = [x for k, x in enumerate(reviewed_ids) if k != i]
            saved = reviewed_ids[i]

            first_recommendations, refined_businesses, explanatory_refs = collaborative_recommender(user)

            copy = []
            for item in first_recommendations:
                copy.append(item)

            second_recommendations = content_based_recommender(temp, refined_businesses, user)

            # Apply a cascade scheme to join the two recommender systems
            final_recommendations = cascade_scheme(first_recommendations, second_recommendations)

            # Novelty
            #   For each recommendation: SUM(-log of the proportion of users who viewed/rated an item)
            #   --------------------------------------------------------------------------------------
            #                            number of recommendations in list
            if not novelty_done:
                num_users = len(users_df)
                # exit()
                numerator = 0
                for item in final_recommendations:
                    business_reviews = reviews_df[reviews_df["business_id"] == item[1]]
                    if len(business_reviews) != 0:
                        numerator += -1 * (math.log2(len(business_reviews)/num_users))
                novelty_h = numerator / len(final_recommendations)
                numerator = 0
                for item in first_recommendations:
                    business_reviews = reviews_df[reviews_df["business_id"] == item[1]]
                    if len(business_reviews) != 0:
                        numerator += -1 * (math.log2(len(business_reviews)/num_users))
                novelty_b = numerator / len(first_recommendations)
                numerator = 0
                for item in second_recommendations:
                    business_reviews = reviews_df[reviews_df["business_id"] == item[1]]
                    if len(business_reviews) != 0:
                        numerator += -1 * (math.log2(len(business_reviews)/num_users))
                novelty_c = numerator / len(second_recommendations)
                novelty_done = True

            # F-Measure
            # 2* ((precision * recall) / (precision + recall))
            # A positive is an item which is recommended
            # precision = True positive / (True Positive + false positive)
            # recall = True positive / (True positive + false negative)
            # Positive / Negative = Recommended / Not Recommended
            # True / False = used / not used ---> used = 3.0+, not used = 2.0-
            for item in final_recommendations:
                if item[1] == saved:
                    id_search = rated[rated["business_id"] == item[1]]
                    actual_rating = id_search['stars'].iloc[0]
                    predicted_rating = item[0]
                    # Detect fp, fn, tp or tn, based on used = 3.0 stars or above, not used = 2.0 stars or below
                    if actual_rating >= 3 and predicted_rating >= 3:
                        tp_h += 1
                    elif actual_rating >= 3 and predicted_rating <= 2:
                        fn_h += 1
                    elif actual_rating <= 2 and predicted_rating <= 2:
                        tn_h += 1
                    elif actual_rating <= 3 and predicted_rating >= 3:
                        fp_h += 1
            for item in first_recommendations:
                if item[1] == saved:
                    id_search = rated[rated["business_id"] == item[1]]
                    actual_rating = id_search['stars'].iloc[0]
                    predicted_rating = item[0]
                    # Detect fp, fn, tp or tn, based on used = 3.0 stars or above, not used = 2.0 stars or below
                    if actual_rating >= 3 and predicted_rating >= 3:
                        tp_b += 1
                    elif actual_rating >= 3 and predicted_rating <= 2:
                        fn_b += 1
                    elif actual_rating <= 2 and predicted_rating <= 2:
                        tn_b += 1
                    elif actual_rating <= 3 and predicted_rating >= 3:
                        fp_b += 1
            for item in second_recommendations:
                if item[1] == saved:
                    id_search = rated[rated["business_id"] == item[1]]
                    actual_rating = id_search['stars'].iloc[0]
                    predicted_rating = item[0]
                    # Detect fp, fn, tp or tn, based on used = 3.0 stars or above, not used = 2.0 stars or below
                    if actual_rating >= 3 and predicted_rating >= 3:
                        tp_c += 1
                    elif actual_rating >= 3 and predicted_rating <= 2:
                        fn_c += 1
                    elif actual_rating <= 2 and predicted_rating <= 2:
                        tn_c += 1
                    elif actual_rating <= 3 and predicted_rating >= 3:
                        fp_c += 1

            # RMSE
            # Find the item which has been removed from reviewed_ids in the recommendations and store it alongside the
            #   actual rating that was given
            for item in final_recommendations:
                if item[1] == saved:
                    id_search = rated[rated["business_id"] == item[1]]
                    actual_rating = id_search['stars'].iloc[0]
                    ratings_comparison_h.append([item[0], actual_rating])
                    break

            # Repeat the process above for only collaborative-filtering for the baseline test
            for item in copy:
                if item[1] == saved:
                    id_search = rated[rated["business_id"] == item[1]]
                    actual_rating = id_search['stars'].iloc[0]
                    ratings_comparison_b.append([item[0], actual_rating])
                    break

            # Repeat the process above for only content-based-filtering for the baseline test
            for item in second_recommendations:
                if item[1] == saved:
                    id_search = rated[rated["business_id"] == item[1]]
                    actual_rating = id_search['stars'].iloc[0]
                    ratings_comparison_c.append([item[0], actual_rating])
                    break

            i += 1


    print("-------------")
    print("RMSE")
    print("-------------")

    # calculate the RMSE for the Hybrid
    sum_dif_squared = 0
    for item in ratings_comparison_h:
        sum_dif_squared += (item[0] - item[1])**2
    rmse = math.sqrt(sum_dif_squared / len(ratings_comparison_h))
    print("Hybrid RMSE: ", rmse)

    # calculate the RMSE for the baseline: collaborative
    sum_dif_squared = 0
    for item in ratings_comparison_b:
        sum_dif_squared += (item[0] - item[1]) ** 2
    rmse = math.sqrt(sum_dif_squared / len(ratings_comparison_b))
    print("Baseline (CF) RMSE: ", rmse)

    # calculate the RMSE for the baseline: content-based
    sum_dif_squared = 0
    for item in ratings_comparison_c:
        sum_dif_squared += (item[0] - item[1]) ** 2
    rmse = math.sqrt(sum_dif_squared / len(ratings_comparison_c))
    print("Baseline (CB) RMSE: ", rmse)
    print()

    # Calculate the f1-score
    print("-------------")
    print("F1-score")
    print("-------------")
    print("Total results: " + str(tp_b + tn_b + fn_b + fp_b))
    precision_h = tp_h / (tp_h + fp_h)
    recall_h = tp_h / (tp_h + fn_h)
    f1_score_h = 2*((precision_h*recall_h)/(precision_h + recall_h))
    print("Hybrid f1-score: " + str(f1_score_h*100) + "%")
    precision_b = tp_b / (tp_b + fp_b)
    recall_b = tp_b / (tp_b + fn_b)
    f1_score_b = 2 * ((precision_b * recall_b) / (precision_b + recall_b))
    print("Baseline (CF) f1-score: "+ str(f1_score_b*100) + "%")
    precision_c = tp_c / (tp_c + fp_c)
    recall_c = tp_c / (tp_c + fn_c)
    f1_score_c = 2 * ((precision_c * recall_c) / (precision_c + recall_c))
    print("Baseline (CB) f1-score: "+ str(f1_score_c*100) + "%")
    print()

    # Calculate the novelty
    print("-------------")
    print("Novelty")
    print("-------------")
    print("Hybrid novelty: ", novelty_h)
    print("Baseline (CF) novelty: ", novelty_b)
    print("Baseline (CB) novelty: ", novelty_c)
    print()

    print("-------------")
    print("Explanability")
    print("-------------")
    print("Total items explained: ", total_explained)
    print("Total items recommended: ", total_recommended)
    print("Explainability proportion: ", str(total_explained / total_recommended))

    print()
    exit()