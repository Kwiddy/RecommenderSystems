# imports
from recommenderOne import *
from recommenderTwo import *
from ast import literal_eval


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
    rank = 1
    all_outputs = pd.DataFrame()
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
            result["Result Rank"] = rank
            result = result.set_index("Result Rank")

            # Remove unnecessary columns
            result = result.drop(columns=["business_id", "latitude", "longitude", "state", "city", "stars", "hours",
                                          "attributes", "is_open", "categories", "review_count"])

            # Add the item to the output
            if first:
                output = result
                all_outputs = pd.concat([all_outputs, result])
                first = False
            else:
                output = pd.concat([output, result])
                all_outputs = pd.concat([all_outputs, result])

            # Increment rank
            rank += 1

        # Print the next batch of recommended items
        print(output)

        # Ensures that the user can only keep displaying more recommendations up until the end of the recommendations
        #       generated.
        postponed_choice = False
        if last_row != results[-1]:
            valid_choice = False
            print("[M] - Display 8 more recommendations")
            print("[S] - See more details about a recommendation")
            print("[F] - Finish")
            while not valid_choice:
                yn = input("Please choose from the options above: ")
                if yn.upper() == "M":
                    valid_choice = True
                    start += 8
                    return_num += 8
                elif yn.upper() == "S":
                    postponed_choice = True
                    more_details(rank, all_outputs, businesses_df)
                    print()
                    print("[M] - Display 8 more recommendations")
                    print("[S] - See more details about a recommendation")
                    print("[F] - Finish")
                elif yn.upper() == "F":
                    valid_choice = True
                    show_more = False
                elif not postponed_choice:
                    print("INVALID INPUT")
        else:
            show_more = False
    print()


# Display more details about a chosen recommendation
def more_details(rank, recommendations, businesses):
    # Check that a valid value has been input
    valid_choice = False
    while not valid_choice:
        business = input("Enter the index (Rank) of the business you wish to see more about [or C to cancel]: ")
        if business != "C" and business != "c":
            try:
                business = int(business)
                if 0 < business < rank:
                    valid_choice = True
            except ValueError:
                valid_choice = False
            if not valid_choice:
                print("INVALID INPUT - Please enter a number shown in the leftmost column of the given recommendations")
        else:
            valid_choice = True

    if business != "C" and business != "c":
        # Locate the business
        result = recommendations.loc[business, :]
        result_name = result["name"]
        result_addr = result["address"]
        result_postal = result["postal_code"]
        full_business = businesses.loc[(businesses['name'] == result_name) & (businesses['address'] == result_addr) &
                                       (businesses['postal_code'] == result_postal)].copy()

        # Print the details of the business in a readable format
        # attributes,hours
        print()
        print("Name: ", full_business.iloc[0]["name"])
        print("ID: ", full_business.iloc[0]["business_id"])
        print("Address: " + str(full_business.iloc[0]["address"]) + ", " + str(full_business.iloc[0]["city"]) + ", " +
              str(full_business.iloc[0]["state"]) + ", " + str(full_business.iloc[0]["postal_code"]))
        print("Stars: " + str(full_business.iloc[0]["stars"]))
        print("Number of Reviews: " + str(full_business.iloc[0]["review_count"]))
        if full_business.iloc[0]["is_open"] == 0:
            open_state = "Closed"
        else:
            open_state = "Open"
        print("Current Status: " + open_state)
        print("Categories: " + str(full_business.iloc[0]["categories"]))

        # Print the opening hours in a user-friendly format
        try:
            hours = literal_eval(full_business.iloc[0]["hours"])

            print("Hours: ")
            for item in hours:
                if item in ["Wednesday", "Thursday", "Saturday"]:
                    to_print = "\t" + item + "\t" + hours[item]
                else:
                    to_print = "\t" + item + "\t\t" + hours[item]
                print(to_print)
        except:
            print()

        # Print the companeis attributes in a user-friendly format
        try:
            attributes = literal_eval(full_business.iloc[0]["attributes"])
            print("Attributes: ")
            for item in attributes:
                to_print = "\t" + item + " " + attributes[item]
                print(to_print)
        except:
            print()

        print()

