# imports
from recommenderOne import *
from recommenderTwo import *


# Create user's recommendations using a hybrid scheme
def generate_recommendations(user_id):
    # Update the dataframes
    reviews_df = pd.read_csv("newDFReview.csv")
    users_df = pd.read_csv("newDFUser.csv")
    businesses_df = pd.read_csv("newDFBusiness.csv")

    # Detect special case where a user has no relevant reviews, in this scenario, return recommendations based purely
    #   on business ratings
    # Check to make sure that some reviews exist
    review_search = reviews_df[reviews_df["user_id"] == user_id]
    if len(review_search) == 0:
        # Just return the highest rated businesses as they appear
        output = businesses_df.copy()
        output = output.sort_values(by=['stars', 'review_count'], ascending=False)
        # print(output[["stars", "review_count"]])
        print(output)
    else:

        recommender_one(user_id)
        recommender_two(user_id)