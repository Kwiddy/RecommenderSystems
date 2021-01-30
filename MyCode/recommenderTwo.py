# This recommender uses content-based filtering

# imports
import pandas as pd

# Method
# 1. Information Source
# 2. Content Analyser
# 3. Represented items -> (Profile Learner & Profiles) + (Filtering Component)
# 4. List of recommendations


def recommender_two(user_id):
    # Update the dataframes
    reviews_df = pd.read_csv("newDFReview.csv")
    users_df = pd.read_csv("newDFUser.csv")
    businesses_df = pd.read_csv("newDFBusiness.csv")

    # Content analyser - Represent items' content in a structured form
    analysis = content_analyser(user_id, users_df, businesses_df, reviews_df)

    # Profile learner - Collect and generalise user preference data and construct user profile

    # Filtering component - Apply user profile model to new item representations
    #   Match user profile representation to item representations
    #   Generate a prediction / relevance judgment / score
    #   Present a (ranked) list of item recommendations


def content_analyser(user_id, users_df, businesses_df, reviews_df):
    return "hi"