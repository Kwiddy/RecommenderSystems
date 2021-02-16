# imports
import pandas as pd
import numpy as np
from ast import literal_eval


# Update user preferences
def update_preferences(user_id, users_df, businesses_df):
    # Display preferences menu and repeat request until a valid input is given
    print("[N] - Change number of recommendations displayed")
    print("[S] - Choose a minimum number of stars for recommendations")
    print("[U] - Update blacklisted sites")
    print("[R] - Recommend previously reviewed items or not")
    print("[C] - Covid preferences")
    print("[A] - Advanced Recommender Preferences")
    print("[B] - Return")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        selection = input("Please enter one of the options above: ")

        # Allow the user to change the default number of recommendations which are displayed
        if selection.upper() == "N":
            print()
            valid_choice = True
            update_display_num(user_id, users_df, businesses_df)

        # Allow the user to choose if they wish the recommender to recommend places they've already reviewed or not
        elif selection.upper() == "R":
            print()
            valid_choice = True
            update_review_seen(user_id, users_df)

        # Allow the user to have a list of blacklisted businesses which won't be recommended
        elif selection.upper() == "U":
            print()
            valid_choice = True
            update_blacklist(user_id, users_df, businesses_df)

        # Allow the user to express a minimum number of stars required for recommendations
        elif selection.upper() == "S":
            print()
            valid_choice = True
            update_min_stars(user_id, users_df)

        # Allow the user to define COVID related preferences
        elif selection.upper() == "C":
            print()
            valid_choice = True
            update_covid_pref(user_id, users_df)

        # Allow the users to refine the recommendations further, e.g. by wheelchair access
        elif selection.upper() == "A":
            print()
            valid_choice = True
            advanced_options(user_id, users_df, businesses_df)

        elif selection.upper() != "B":
            # Allow the user to exit the program
            if selection.upper() == "X":
                valid_choice = True
                exit()

            # Otherwise display an error message
            else:
                print("INVALID INPUT")

        # Allow the user to return to the main menu
        else:
            valid_choice = True
    print()


# Preference: Allow the user to define COVID-related preferences for recommendations
def update_covid_pref(user, users_df):
    # Display Covid preferences menu and repeat request until a valid input is given
    print("[T] - Preference for only recommending places that offer takeout or delivery")
    print("[C] - Preference for only recommending places that are not temporarily closed")
    print("[B] - Return")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        selection = input("Please enter one of the options above: ")

        # Preference for only recommending places that offer takeout or delivery
        if selection.upper() == "T":
            print()
            valid_choice = True

            # Find the current preference (default: Yes (Yes, they do wish reviewed items to be recommended))
            id_search = users_df[users_df["user_id"] == user]
            current_status = id_search['covid_d_t'].iloc[0]

            # Convert to text so easier for user to understand
            if current_status == "Y":
                current_status = "YES"
            else:
                current_status = "NO"

            # Allow user to make choice
            valid_input = False
            while not valid_input:
                yn = input(
                    "Would you like only places which offer takeout or delivery during COVID to be recommended to you "
                    "if they are suitable? [Y/N or C to cancel] (Currently " + current_status + "): ")
                if yn.upper() == "Y":
                    valid_input = True
                    users_df.loc[users_df["user_id"] == user, "covid_d_t"] = yn.upper()
                    print("Preference has been changed to: YES")
                    users_df.to_csv("newDFUser.csv", index=0)
                elif yn.upper() == "N":
                    valid_input = True
                    users_df.loc[users_df["user_id"] == user, "covid_d_t"] = yn.upper()
                    print("Preference has been changed to: NO")
                    users_df.to_csv("newDFUser.csv", index=0)
                elif yn.upper() == "C":
                    valid_input = True
                else:
                    print("INVALID INPUT")

        # Preference for only recommending places that are not temporarily closed
        elif selection.upper() == "C":
            print()
            valid_choice = True
            # Find the current preference (default: Yes (Yes, they do wish reviewed items to be recommended))
            id_search = users_df[users_df["user_id"] == user]
            current_status = id_search['covid_temp_closed'].iloc[0]

            # Convert to text so easier for user to understand
            if current_status == "Y":
                current_status = "YES"
            else:
                current_status = "NO"

            # Allow user to make choice
            valid_input = False
            while not valid_input:
                yn = input(
                    "Would you like only places which are not temporarily closed during COVID to be recommended to you "
                    "if they are suitable? [Y/N or C to cancel] (Currently " + current_status + "): ")
                if yn.upper() == "Y":
                    valid_input = True
                    users_df.loc[users_df["user_id"] == user, "covid_temp_closed"] = yn.upper()
                    print("Preference has been changed to: YES")
                    users_df.to_csv("newDFUser.csv", index=0)
                elif yn.upper() == "N":
                    valid_input = True
                    users_df.loc[users_df["user_id"] == user, "covid_temp_closed"] = yn.upper()
                    print("Preference has been changed to: NO")
                    users_df.to_csv("newDFUser.csv", index=0)
                elif yn.upper() == "C":
                    valid_input = True
                else:
                    print("INVALID INPUT")

        elif selection.upper() != "B":
            # Allow the user to exit the program
            if selection.upper() == "X":
                valid_choice = True
                exit()

            # Otherwise display an error message
            else:
                print("INVALID INPUT")

        # Allow the user to return to the main menu
        else:
            valid_choice = True
    print()

# Preference: Define if they wish to have items recommended which they've already reviewed
def update_review_seen(user, users_df):
    # Find the current preference (default: Yes (Yes, they do wish reviewed items to be recommended))
    id_search = users_df[users_df["user_id"] == user]
    current_status = id_search['recommend_seen'].iloc[0]

    # Convert to text so easier for user to understand
    if current_status == "Y":
        current_status = "YES"
    else:
        current_status = "NO"

    # Allow user to make choice
    valid_input = False
    while not valid_input:
        yn = input("Would you like your previously recommended bars to be recommended to you if they are suitable? "
                   "[Y/N or C to cancel] (Currently " + current_status + "): ")
        if yn.upper() == "Y":
            valid_input = True
            users_df.loc[users_df["user_id"] == user, "recommend_seen"] = yn.upper()
            print("Preference has been changed to: YES")
            users_df.to_csv("newDFUser.csv", index=0)
        elif yn.upper() == "N":
            valid_input = True
            users_df.loc[users_df["user_id"] == user, "recommend_seen"] = yn.upper()
            print("Preference has been changed to: NO")
            users_df.to_csv("newDFUser.csv", index=0)
        elif yn.upper() == "C":
            valid_input = True
        else:
            print("INVALID INPUT")


# Preference: Allow further refinement of businesses to recommend
def advanced_options(user, users_df, businesses_df):
    # Find the current preferences
    id_search = users_df[users_df["user_id"] == user]
    preferences = id_search['advanced_preferences'].iloc[0]

    # print(preferences)
    # Retrieve and display their existing preferences
    try:
        preferences = literal_eval(preferences)
        print("Your current preferences:")
        for preference in preferences:
            print(preference + ": " + str(preferences[preference]))
        print()
    except:
        if np.isnan(preferences):
            preferences = {}
            print("You have not yet specified any particular preferences")
        else:
            preferences = literal_eval(preferences)
            print("Your current preferences:")
            for preference in preferences:
                print(preference + ": " + str(preferences[preference]))
            print()

    # Present menu and take valid input of user's choicer
    print("[A] - Add / Amend advanced preferences")
    print("[D] - Delete an advanced preference")
    print("[B] - Return")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        choice = input("Please enter one of the options above: ")

        # Allow the user to add and delete advanced preferences
        if choice.upper() == "A":
            print()
            valid_choice = True
            add_preference(preferences, businesses_df, users_df, user)
            anything_else(user, users_df, businesses_df)

        # Allow the user to delete an existing advanced preference
        elif choice.upper() == "D":
            print()
            valid_choice = True
            delete_preference(user, users_df, preferences)
            anything_else(user, users_df, businesses_df)


        # Detect invalid inputs or a wish to close the program
        elif choice.upper() != "B":
            if choice.upper() == "X":
                print("Closing program...")
                valid_choice = True
                exit()
            else:
                print("INVALID INPUT - Please select from the options above")

        # Allow the user to return from this section
        else:
            valid_choice = True
            print()


# Allow user to delete their advanced preferences
def delete_preference(user, users_df, preferences):
    # Present the current preferences to choose from
    for item in preferences:
        print(item + " (Currently: " + preferences[item] + ")")
        saved_example = item

    # Allow the user to select one to delete
    valid_choice = False
    while not valid_choice:
        choice = input("Please enter an entry to be removed, for example: " + saved_example + ", (or [C] to cancel): ")
        if choice.upper() != "C":
            if preferences.get(choice) is not None:
                valid_choice = True
        else:
            valid_choice = True
        if not valid_choice:
            print("INVALID INPUT")

    if choice.upper() != "C":
        # Remove the chosen preference
        preferences.pop(choice)

        # Save the updated preferences to the user's profile
        users_df.loc[users_df["user_id"] == user, "advanced_preferences"] = str(preferences)
        users_df.to_csv("newDFUser.csv", index=0)

        # Notify user
        print("Your preferences have been updated...")


# Allow user to add an advanced preference, these align with disabilities and additional requirements
def add_preference(preferences, businesses, users, user_id):
    # options:
    # OutdoorSeating, Delivery, Takeout, GoodForKids, WheelchairAccessible, DogsAllowed, Smoking, NoiseLevel, Alcohol,
    options = {"1": "OutdoorSeating", "2": "Delivery", "3": "RestaurantsTakeOut", "4": "GoodForKids",
               "5": "WheelchairAccessible", "6": "DogsAllowed", "7": "Smoking", "8": "NoiseLevel", "9": "Alcohol"}
    print("[1] - Outdoor Seating")
    print("[2] - Delivery")
    print("[3] - Takeout")
    print("[4] - Good for Kids")
    print("[5] - Wheelchair Accessible")
    print("[6] - Dogs Allowed")
    print("[7] - Smoking")
    print("[8] - Noise Level")
    print("[9] - Alcohol")

    # Request that they enter one of the options above
    valid_choice = False
    while not valid_choice:
        choice = input("Please enter one of the options above [or C to cancel]: ")
        if choice.upper() != "C":
            try:
                temp = int(choice)
                if 0 < temp < 10:
                    valid_choice = True
                else:
                    print("INVALID INPUT - Please enter one of the numbers above")
            except:
                print("INVALID INPUT - Please enter one of the numbers above")
                valid_choice = False
        else:
            valid_choice = True

    if choice.upper() != "C":
        # Check to see if user already has a preference for this selection
        no_change = False
        if preferences.get(options[choice]) is not None:
            valid = False
            current_choice = preferences.get(options[choice])
            while not valid:
                yn = input("You have already expressed a preference for this (Choice: " + str(current_choice)
                           + "), do you wish to change it [Y/N]?: ")
                if yn.upper() == "Y":
                    valid = True
                elif yn.upper() == "N":
                    valid = True
                    no_change = True
                else:
                    print("INVALID INPUT - Please enter [Y] for Yes, or [N] for No")

    # Find the advanced preference they have chosen and then find the available options for that choice
    if choice.upper() != "C":
        if not no_change:
            chosen = options[choice]

            options = []
            for index, row in businesses.iterrows():
                try:
                    attrib_dict = literal_eval(row["attributes"])
                    try:
                        row_val = attrib_dict[chosen]
                        if row_val not in options:
                            options.append(row_val)
                    except:
                        pass
                except:
                    pass

            selection = []
            # Remove old u' strings
            for item in options:
                if item.startswith("u'"):
                    selection.append(item[2:-1])
                elif item[0] == "'" and item[-1] == "'":
                    selection.append(item[1:-1])
                else:
                    selection.append(item)

            # Remove duplicates
            selection = list(dict.fromkeys(selection))

            # Print the options to the screen
            print("The options for this are: ")
            count = 1
            for item in selection:
                print("[" + str(count) + "] - " + item.replace("_", " "))
                count += 1

            # Allow them to specify one of the options or cancel
            valid_choice = False
            while not valid_choice:
                choice = input("Please enter your selection from above [1-" + str(len(selection))
                               + "] (or [C] to cancel): ")
                if choice.upper() != "C":
                    try:
                        if int(choice) != 0:
                            try:
                                chosen_preference = selection[int(choice)-1]
                                valid_choice = True
                            except:
                                pass
                    except ValueError:
                        pass
                    if not valid_choice:
                        print("INVALID INPUT")
                else:
                    valid_choice = True

            if choice.upper() != "C":
                # If the preference is already in list of their preferences then change it, otherwise add it
                preferences[chosen] = chosen_preference

                # Save the new user preferences
                users.loc[users["user_id"] == user_id, "advanced_preferences"] = str(preferences)
                users.to_csv("newDFUser.csv", index=0)
                print("Your preferences have been updated")
                print()


# Preference: define a minimum number of stars required
def update_min_stars(user, users_df):
    # Find the current number of stars required (default: 1)
    id_search = users_df[users_df["user_id"] == user]
    min_stars = id_search['min_stars'].iloc[0]

    # Allow the input to input their chosen number of stars in the range [1-5]
    #   Must be an integer. The user can also cancel and return to the menu if wished
    valid_input = False
    while not valid_input:
        choice = input("Enter a minimum number of stars for recommendations [1-5, or [C] to cancel] (Current: " + str(min_stars) + "): ")
        if choice.upper() != "C":
            try:
                if int(choice) in range(1, 6):
                    valid_input = True
                    temp = int(choice)
            except ValueError:
                print("INVALID INPUT")
                valid_input = False
        else:
            valid_input = True

    # Update the minimum number of stars to the new value and update the dataframe
    if choice.upper() != "C":
        users_df.loc[users_df["user_id"] == user, "min_stars"] = str(choice)
        print("Number of stars given has been changed to: ", choice)
        users_df.to_csv("newDFUser.csv", index=0)


# Preference: store a list of blacklisted sites
def update_blacklist(user_id, users_df, businesses_df):
    # Retrieve the user's current list of blacklisted businesses, stored as a string
    id_search = users_df[users_df["user_id"] == user_id]
    blacklist = id_search['blacklist'].iloc[0]

    # Custom blacklist printing to display the currently blacklisted sites to the user
    current_blacklist_arr = []
    if not pd.isna(blacklist):
        current_blacklist_arr = blacklist.split(",")

        names = []
        for item in current_blacklist_arr:
            business_found = businesses_df[businesses_df["business_id"] == item]
            name = business_found['name'].iloc[0]
            names.append(name)

        data = {'business_id': current_blacklist_arr, 'business_name': names}
        output_df = pd.DataFrame(data, columns=['business_id', 'business_name'])
        print(output_df)
        print()

    # Take user input on how they wish to edit the list of blacklisted sites, continue requested until valid input is
    #       given or this section is closed
    print("[A] - Add to blacklist")
    print("[D] - Delete from blacklist")
    print("[B] - Return")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        choice = input("Please select one of the options above: ")

        # Allow the user to add a new business to the blacklist, they may also cancel if they wish
        if choice.upper() == "A":
            valid_choice = True
            valid_id = False
            while not valid_id:
                blacklisted_id = input("Enter the id of the business to blacklist (or [C] to cancel): ")

                # Check that a valid list has been inputted
                if blacklisted_id.upper() != "C":
                    business_found = businesses_df[businesses_df["business_id"] == blacklisted_id]
                    if len(business_found) != 0:
                        valid_id = True
                    else:
                        print("INVALID ID")
                else:
                    valid_id = True

            # Append the new business to the blacklist and update the dataframe
            if blacklisted_id.upper() != "C":
                current_blacklist_arr.append(blacklisted_id)
                users_df.loc[users_df["user_id"] == user_id, "blacklist"] = ",".join(current_blacklist_arr)
                users_df.to_csv("newDFUser.csv", index=0)
                print("Added to blacklist")

        # Allow the user to delete a business from the blacklist, they may also cancel if they wish
        elif choice.upper() == "D":
            if len(current_blacklist_arr) != 0:
                valid_choice = True
                valid_int = False

                # The user inputs a value corresponding to the index on the blacklist
                while not valid_int:
                    # Determine the possible options for deletion
                    if len(current_blacklist_arr) != 1:
                        possible_options = "[0-" + str(len(current_blacklist_arr) - 1) + "]"
                    else:
                        possible_options = "[0]"

                    # Allow the user to input their chosen value
                    choice = input("Enter the index of the business you wish to remove " + possible_options +
                                   " (or [C] to cancel):")

                    # Check that a valid index has been inputted and send an error message or delete the business as
                    #   appropriate
                    if choice.upper() != "C":
                        try:
                            choice = int(choice)
                            valid_int = True
                            del current_blacklist_arr[choice]
                            users_df.loc[users_df["user_id"] == user_id, "blacklist"] = ",".join(current_blacklist_arr)
                            users_df.to_csv("newDFUser.csv", index=0)
                        except ValueError:
                            print("INVALID INPUT - Must be an integer in the range shown above")
                    else:
                        valid_int = True

                # Update and save the dataframe
                if choice.upper() != "C":
                    users_df.loc[users_df["user_id"] == user_id, "blacklist"] = ",".join(current_blacklist_arr)
                    users_df.to_csv("newDFUser.csv", index=0)

            # Special case: display a message if the blacklist is currently empty for that user
            else:
                print("Your blacklist is already empty")

        elif choice.upper() != "B":
            # Allow the user to exit the program
            if choice.upper() == "X":
                valid_choice = True
                exit()

            # Display an invalid input message where appropriate
            else:
                print("INVALID INPUT")

        # Allow the user to return to the menu
        else:
            valid_choice = True
    print()


# Preference: choose the number of recommendations to be displayed
def update_display_num(user_id, users_df, businesses_df):
    # Retrieve the current preference (default: 8)
    id_search = users_df[users_df["user_id"] == user_id]
    to_display = id_search['display_num'].iloc[0]

    # Keep requesting until a valid input is given, the user may cancel this if they wish
    valid_choice = False
    while not valid_choice:
        response = input("Please enter the number of recommendations to show (Current: " + str(
            to_display) + ") (or [C] to cancel): ")
        if response != "":
            # Allow the user to cancel their selection
            if response.upper() == "C":
                valid_choice = True
            else:
                # Determine if a valid number of recommendations has been inputted
                try:
                    to_display = int(response)
                    valid_choice = True
                except ValueError:
                    print("INVALID INPUT")
        # If nothing is inputted then the existing preference is used
        else:
            valid_choice = True

    # Update the users dataframe and notify the user
    if response.upper() != "C":
        if response.upper() != "":
            users_df.loc[users_df["user_id"] == user_id, "display_num"] = to_display
            print("Preferred number of recommendations changed to: ", to_display)
            anything_else(user_id, users_df, businesses_df)
            users_df.to_csv("newDFUser.csv", index=0)
        else:
            print("Your preferences have not been changed")


# Ask the user if they wish to change any more of their preferences
def anything_else(user_id, users_df, businesses_df):
    print()
    yn = input("Are there any other preferences you would like to change? [Y/N]: ")
    # Repeat the request until a valid input is given
    valid_choice = False
    while not valid_choice:
        if yn.upper() == "Y":
            valid_choice = True
            update_preferences(user_id, users_df, businesses_df)
        elif yn.upper() == "N":
            valid_choice = True
        else:
            yn = input("INVALID INPUT - Please select Yes [Y] or No [N]: ")