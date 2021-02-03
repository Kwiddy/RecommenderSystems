# imports
from collaborativeRecommender import *
from contentBasedRecommender import *
from ast import literal_eval
import numpy as np


# Create user's recommendations using a hybrid scheme
def generate_recommendations(user_id, users_df):
    # Update the dataframes
    reviews_df = pd.read_csv("newDFReview.csv")
    users_df = pd.read_csv("newDFUser.csv")
    businesses_df = pd.read_csv("newDFBusiness.csv")

    # To display is the users preference for the number of results to show
    id_search = users_df[users_df["user_id"] == user_id]
    to_display = id_search['display_num'].iloc[0]

    # Display a small explanation of results
    # Including how data and reviews are used, and the user's preferences and advanced preferences?
    display_explanation(user_id, users_df)

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

        first_recommendations = collaborative_recommender(user_id)

        ############

        display_results(first_recommendations, businesses_df, to_display)

        ############

        content_based_recommender(user_id)


# Display the results from the recommender
def display_results(results, businesses_df, return_num):
    show_more = True
    start = 0
    end = return_num
    rank = 1
    all_outputs = pd.DataFrame()
    # The show more loop allows the user to continuously display more recommendations
    while show_more:
        output = pd.DataFrame()
        first = True

        # Display the next n items from the sorted list of recommendations
        for item in results[start:end]:
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

        # Print the next batch of recommended items (in such a way that ellipses aren't used and all rows are printed)
        with pd.option_context('display.max_rows', None):
            print(output)

        # Ensures that the user can only keep displaying more recommendations up until the end of the recommendations
        #       generated.
        postponed_choice = False
        if last_row != results[-1]:
            valid_choice = False
            print("[M] - Display " + str(return_num) + " more recommendations")
            print("[S] - See more details about a recommendation")
            print("[F] - Finish")
            while not valid_choice:
                yn = input("Please choose from the options above: ")
                if yn.upper() == "M":
                    valid_choice = True
                    start += return_num
                    end += return_num
                elif yn.upper() == "S":
                    postponed_choice = True
                    more_details(rank, all_outputs, businesses_df)
                    print()
                    print("[M] - Display " + str(return_num) + " more recommendations")
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

    # Print the details of the business in a readable format
    if business != "C" and business != "c":
        # Locate the business
        result = recommendations.loc[business, :]
        result_name = result["name"]
        result_addr = result["address"]
        result_postal = result["postal_code"]
        full_business = businesses.loc[(businesses['name'] == result_name) & (businesses['address'] == result_addr) &
                                       (businesses['postal_code'] == result_postal)].copy()

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
                if item == "OutdoorSeating":
                    if attributes[item] == "True":
                        print("\t- Has outdoor seating")
                    else:
                        print("\t- Does not have outdoor seating")
                elif item == "HasTV":
                    if attributes[item] == "True":
                        print("\t- Has a TV")
                    else:
                        print("\t- Does not have a TV")
                elif item == "RestaurantsGoodForGroups":
                    if attributes[item] == "True":
                        print("\t- Good for groups")
                    else:
                        print("\t- Not good for groups")
                elif item == "HappyHour":
                    if attributes[item] == "True":
                        print("\t- Has a Happy Hour")
                    else:
                        print("\t- Does not have a Happy Hour")
                elif item == "RestaurantsDelivery":
                    if attributes[item] == "True":
                        print("\t- Does delivery")
                    else:
                        print("\t- Does not do delivery")
                elif item == "RestaurantsTakeOut":
                    if attributes[item] == "True":
                        print("\t- Does takeout")
                    else:
                        print("\t- Does not do takeout")
                elif item == "GoodForKids":
                    if attributes[item] == "True":
                        print("\t- Good for kids")
                    else:
                        print("\t- Not Good for kids")
                elif item == "BikeParking":
                    if attributes[item] == "True":
                        print("\t- Has bike parking")
                    else:
                        print("\t- Does not have bike parking")
                elif item == "Caters":
                    if attributes[item] == "True":
                        print("\t- Has catering")
                    else:
                        print("\t- Does not have catering")
                elif item == "WheelchairAccessible":
                    if attributes[item] == "True":
                        print("\t- Is wheelchair accessible")
                    else:
                        print("\t- Is not wheelchair accessible")
                elif item == "DriveThru":
                    if attributes[item] == "True":
                        print("\t- Has a drive-through")
                    else:
                        print("\t- Does not have a drive-through")
                elif item == "CoatCheck":
                    if attributes[item] == "True":
                        print("\t- Has coat checking")
                    else:
                        print("\t- Does not have coat checking")
                elif item == "DogsAllowed":
                    if attributes[item] == "True":
                        print("\t- Dogs are allowed")
                    else:
                        print("\t- Dogs are not allowed")
                elif item == "RestaurantsPriceRange2":
                    print("\t- Price Range: " + str(attributes[item]))
                elif item == "Ambience":
                    ambience_dict = literal_eval(attributes[item])
                    descriptors = []
                    for ambience in ambience_dict:
                        if ambience_dict[ambience]:
                            descriptors.append(ambience)
                    if len(descriptors) != 0:
                        keywords = ""
                        for description in descriptors:
                            keywords += description + " "
                        print("\t- Ambience: " + keywords)
                elif item == "Music":
                    music_dict = literal_eval(attributes[item])
                    descriptors = []
                    for music in music_dict:
                        if music_dict[music]:
                            descriptors.append(music)
                    if len(descriptors) != 0:
                        keywords = ""
                        for description in descriptors:
                            keywords += description + " "
                        print("\t- Music: " + keywords)
                elif item == "RestaurantsReservations":
                    if attributes[item] == "True":
                        print("\t- Allows reservations")
                    else:
                        print("\t- Does not allow reservations")
                elif item == "BusinessAcceptsCreditCards":
                    if attributes[item] == "True":
                        print("\t- Accepts credit cards")
                    else:
                        print("\t- Does not accept credit cards")
                elif item == "GoodForDancing":
                    if attributes[item] == "True":
                        print("\t- Good for dancing")
                    else:
                        print("\t- Not good for dancing")
                elif item == "RestaurantsTableService":
                    if attributes[item] == "True":
                        print("\t- Table Service")
                    else:
                        print("\t- No table service")
                elif item == "ByAppointmentOnly":
                    if attributes[item] == "False":
                        print("\t- Appointment Only")
                elif item == "WiFi":
                    to_add = attributes[item]
                    if attributes[item].startswith("u'"):
                        print("\t- Wifi: " + str(to_add[2:-1]))
                    else:
                        print("\t- WiFi: " + to_add)
                elif item == "Smoking":
                    to_add = attributes[item]
                    if attributes[item].startswith("u'"):
                        print("\t- Smoking: " + str(to_add[2:-1]))
                    else:
                        print("\t- Smoking: " + to_add)
                elif item == "RestaurantsAttire":
                    to_add = attributes[item]
                    if attributes[item].startswith("u'"):
                        print("\t- Restaurant Attire: " + str(to_add[2:-1]))
                    else:
                        print("\t- Restaurant Attire: " + to_add)
                elif item == "NoiseLevel":
                    to_add = attributes[item]
                    if attributes[item].startswith("u'"):
                        print("\t- Noise Level: " + str(to_add[2:-1]))
                    else:
                        print("\t- Noise Level: " + to_add)
                elif item == "Alcohol":
                    to_add = attributes[item]
                    to_add = to_add.replace("_", " ")
                    if attributes[item].startswith("u'"):
                        print("\t- Alcohol: " + str(to_add[2:-1]))
                    else:
                        print("\t- Alcohol: " + to_add)
                elif item == "GoodForMeal":
                    meal_dict = literal_eval(attributes[item])
                    descriptors = []
                    for meal in meal_dict:
                        if meal_dict[meal]:
                            descriptors.append(meal)
                    if len(descriptors) != 0:
                        keywords = ""
                        for description in descriptors:
                            keywords += description + " "
                        print("\t- Notably good for meals: " + keywords)
                elif item == "BestNights":
                    nights_dict = literal_eval(attributes[item])
                    descriptors = []
                    for night in nights_dict:
                        if nights_dict[night]:
                            descriptors.append(night)
                    if len(descriptors) != 0:
                        keywords = ""
                        for description in descriptors:
                            keywords += description + " "
                        print("\t- Best Nights: " + keywords)
                elif item == "BusinessParking":
                    parking_dict = literal_eval(attributes[item])
                    descriptors = []
                    for parking_type in parking_dict:
                        if parking_dict[parking_type]:
                            descriptors.append(parking_type)
                    if len(descriptors) != 0:
                        keywords = ""
                        for description in descriptors:
                            keywords += description + " "
                        print("\t- Business parking options: " + keywords)
                    else:
                        print("\t- No business parking available")
                else:
                    to_print = "\t- " + item + " " + attributes[item]
                    print(to_print)
        except:
            print()

        print()


# Show a brief statement explaining how the recommendations have been generated
def display_explanation(user, users_df):
    # Print a brief explanation of results
    print("EXPLANATION OF RESULTS")
    print("The below recommendations have been generated by combining your existing reviews and ratings with the Yelp"
          "database of Sports Bars in Toronto. The data used has taken the COVID-19 pandemic into account and only "
          "considers reviews left during the year of 2019. Along with your reviews, your preferences and advanced "
          "preferences have been taken into account so that the system does not recommend unwanted locations. All "
          "appropriate businesses have then been ranked accordingly to suitability and will be displayed as requested.")

    # Display an overview of the preferences chosen:
    #   number of recommendations to display, blacklist, minimum number of stars, recommending seen items,
    #   and advanced preferences
    id_search = users_df[users_df["user_id"] == user]
    display_num = id_search['display_num'].iloc[0]
    blacklist = id_search['blacklist'].iloc[0]
    min_stars = id_search['min_stars'].iloc[0]
    recommend_seen = id_search['recommend_seen'].iloc[0]
    advanced_preferences = id_search['advanced_preferences'].iloc[0]

    try:
        if math.isnan(blacklist):
            blacklist_out = "You have no items in your blacklist."
    except:
        blacklist = blacklist.split(",")
        if len(blacklist) == 1:
            blacklist_out = "You have one item in your blacklist."
        else:
            blacklist_out = "You have " + str(len(blacklist)) + " items in your blacklist."

    display_num_out = "Your account is set to display " + str(display_num) + " recommendations at a time."

    if int(min_stars) == 1:
        min_stars_out = "All businesses will be considered regardless of their rating."
    elif int(min_stars) == 5:
        min_stars_out = "Only 5 star rated businesses will be considered."
    else:
        min_stars_out = "Only businesses with " + str(min_stars) + " or more stars will be considered."

    if recommend_seen.upper() == "Y":
        recommend_seen_out = "Businesses which you have already reviewed will be recommended."
    else:
        recommend_seen_out = "Only businesses which you have not yet reviewed will be recommended."
    print()

    # Display the informative message
    print("YOUR PREFERENCES TAKEN INTO CONSIDERATION:")
    print(blacklist_out + " " + display_num_out + " " + min_stars_out + " " + recommend_seen_out)
    print()

    # Interpret and print the advanced preferences if appropriate
    try:
        preferences = literal_eval(advanced_preferences)
        print("Your advanced preferences:")
        for preference in preferences:
            print("\t-" + preference + ": " + str(preferences[preference]))
        print()
    except:
        if np.isnan(advanced_preferences):
            print("You have not specified any particular preferences")

    # Outline the recommendation techniques used
    print("Recommender method used: Hybrid recommender (Collaborative and Content-Based), utilising a Cascade scheme")
    print()