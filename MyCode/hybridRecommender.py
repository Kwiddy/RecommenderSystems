# imports
from recommenderOne import *
from recommenderTwo import *


# Create user's recommendations using a hybrid scheme
def generate_recommendations(user_id):
    # Update the dataframes
    reviews_df = pd.read_csv("newDFReview.csv")
    users_df = pd.read_csv("newDFUser.csv")
    businesses_df = pd.read_csv("newDFBusiness.csv")

    # To display is the users preference for the number of results to show
    id_search = users_df[users_df["user_id"] == user_id]
    to_display = id_search['display_num'].iloc[0]

    # Detect special case where a user has no relevant reviews, in this scenario, return recommendations based purely
    #   on business ratings
    # Check to make sure that some reviews exist
    review_search = reviews_df[reviews_df["user_id"] == user_id]
    if len(review_search) == 0:
        # Just return the highest rated businesses as they appear
        output = businesses_df.copy()
        output = output.sort_values(by=['stars', 'review_count'], ascending=False)
        # print(output[["stars", "review_count"]])
        result = []
        for index, row in output.iterrows():
            result.append([1.0, row["business_id"]])
        display_results(result, businesses_df, to_display)
    else:

        first_recommendations = recommender_one(user_id)

        ############

        display_results(first_recommendations, businesses_df, to_display)

        ############

        recommender_two(user_id)


# Display the results from the recommender
def display_results(results, businesses_df, return_num):
    show_more = True
    start = 0
    # The show more loop allows the user to continuously display more recommendations
    while show_more:
        output = pd.DataFrame()
        first = True

        # Display the next n items from the sorted list of recommendations
        for item in results[start:return_num]:
            # Format the item for outputting
            last_row = item
            item_id = item[1]
            result = businesses_df.loc[businesses_df["business_id"] == item_id].copy()
            result["Prediction"] = item[0]

            # Add the item to the output
            if first:
                output = result
                first = False
            else:
                output = pd.concat([output, result])

        # Print the next back of recommended items
        print(output)

        # Ensures that the user can only keep displaying more recommendations up until the end of the recommendations
        #       generated.
        if last_row != results[-1]:
            valid_choice = False
            while not valid_choice:
                yn = input("Display 8 more recommendations? [Y/N]: ")
                if yn.upper() == "Y":
                    valid_choice = True
                    start += 8
                    return_num += 8
                elif yn.upper() == "N":
                    valid_choice = True
                    show_more = False
                else:
                    print("INVALID INPUT")
        else:
            show_more = False
    print()