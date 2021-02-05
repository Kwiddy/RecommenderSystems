# This recommender uses content-based filtering

# imports
import pandas as pd

# Method
# 1. Information Source
# 2. Content Analyser
# 3. Represented items -> (Profile Learner & Profiles) + (Filtering Component)
# 4. List of recommendations


def content_based_recommender(user_id):
    # Update the dataframes
    reviews_df = pd.read_csv("newDFReview.csv")
    users_df = pd.read_csv("newDFUser.csv")
    businesses_df = pd.read_csv("newDFBusiness.csv")

    return temporary_recommender(businesses_df)

    # Content analyser - Represent items' content in a structured form
    analysis = content_analyser(user_id, users_df, businesses_df, reviews_df)

    # Profile learner - Collect and generalise user preference data and construct user profile

    # Filtering component - Apply user profile model to new item representations
    #   Match user profile representation to item representations
    #   Generate a prediction / relevance judgment / score
    #   Present a (ranked) list of item recommendations


def content_analyser(user_id, users_df, businesses_df, reviews_df):
    return "hi"


def temporary_recommender(businesses_df):
    rank = 1
    temp_rankings = []
    for index, row in businesses_df.iterrows():
        temp_rankings.append([rank, row["business_id"]])
        rank += 1
    temp_rankings = sorted(temp_rankings, reverse=True)
    return temp_rankings