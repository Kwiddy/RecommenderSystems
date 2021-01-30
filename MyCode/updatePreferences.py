# imports
import pandas as pd


# Update user preferences
def update_preferences(user_id, users_df, businesses_df):
    # Display preferences menu and repeat request until a valid input is given
    print("[N] - Change number of recommendations displayed")
    print("[S] - Choose a minimum number of stars for recommendations")
    print("[U] - Update blacklisted sites")
    print("[R] - Recommend previously reviewed items or not")
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
                    choice = int(choice)
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
    # Retrieve the user's current list of blacklisted sites, stored as a string
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