import pandas as pd


def update_preferences(user_id, users_df, businesses_df):
    print("[N] - Change number of recommendations displayed")
    print("[S] - Choose a minimum number of stars for recommendations")
    print("[U] - Update blacklisted sites")
    print("[B] - Return")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        selection = input("Please enter one of the options above: ")
        if selection.upper() == "N":
            print()
            valid_choice = True
            update_display_num(user_id, users_df, businesses_df)
        elif selection.upper() == "U":
            print()
            valid_choice = True
            update_blacklist(user_id, users_df, businesses_df)
        elif selection.upper() == "S":
            print()
            valid_choice = True
            update_min_stars(user_id, users_df)
        elif selection.upper() != "B":
            if selection.upper() == "X":
                valid_choice = True
                exit()
            else:
                print("INVALID INPUT")
        else:
            valid_choice = True
    print()


def update_min_stars(user, users_df):
    id_search = users_df[users_df["user_id"] == user]
    min_stars = id_search['min_stars'].iloc[0]

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

    if choice.upper() != "C":
        users_df.loc[users_df["user_id"] == user, "min_stars"] = str(choice)
        print("Number of stars given has been changed to: ", choice)
        users_df.to_csv("newDFUser.csv", index=0)


def update_blacklist(user_id, users_df, businesses_df):
    id_search = users_df[users_df["user_id"] == user_id]
    blacklist = id_search['blacklist'].iloc[0]

    # Custom blacklist printing
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

    print("[A] - Add to blacklist")
    print("[D] - Delete from blacklist")
    print("[B] - Return")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        choice = input("Please select one of the options above: ")
        if choice.upper() == "A":
            valid_choice = True
            valid_id = False
            while not valid_id:
                blacklisted_id = input("Enter the id of the business to blacklist (or [C] to cancel): ")
                if blacklisted_id.upper() != "C":
                    business_found = businesses_df[businesses_df["business_id"] == blacklisted_id]
                    if len(business_found) != 0:
                        valid_id = True
                    else:
                        print("INVALID ID")
                else:
                    valid_id = True
            if blacklisted_id.upper() != "C":
                current_blacklist_arr.append(blacklisted_id)
                users_df.loc[users_df["user_id"] == user_id, "blacklist"] = ",".join(current_blacklist_arr)
                users_df.to_csv("newDFUser.csv", index=0)
                print("Added to blacklist")

        elif choice.upper() == "D":
            if len(current_blacklist_arr) != 0:
                valid_choice = True
                valid_int = False
                while not valid_int:
                    if len(current_blacklist_arr) != 1:
                        possible_options = "[0-" + str(len(current_blacklist_arr) - 1) + "]"
                    else:
                        possible_options = "[0]"
                    choice = input("Enter the index of the business you wish to remove " + possible_options +
                                   " (or [C] to cancel):")
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
                if choice.upper() != "C":
                    users_df.loc[users_df["user_id"] == user_id, "blacklist"] = ",".join(current_blacklist_arr)
                    users_df.to_csv("newDFUser.csv", index=0)
            else:
                print("Your blacklist is already empty")

        elif choice.upper() != "B":
            if choice.upper() == "X":
                valid_choice = True
                exit()
            else:
                print("INVALID INPUT")
        else:
            valid_choice = True
    print()


def update_display_num(user_id, users_df, businesses_df):

    id_search = users_df[users_df["user_id"] == user_id]
    to_display = id_search['display_num'].iloc[0]

    valid_choice = False
    while not valid_choice:
        response = input("Please enter the number of recommendations to show (Current: " + str(
            to_display) + ") (or [C] to cancel): ")
        if response != "":
            if response.upper() == "C":
                valid_choice = True
            else:
                try:
                    to_display = int(response)
                    valid_choice = True
                except ValueError:
                    print("INVALID INPUT")
        else:
            valid_choice = True

    if response.upper() != "C":
        users_df.loc[users_df["user_id"] == user_id, "display_num"] = to_display
        print("Preferred number of recommendations changed to: ", to_display)
        anything_else(user_id, users_df, businesses_df)
        users_df.to_csv("newDFUser.csv", index=0)


def anything_else(user_id, users_df, businesses_df):
    print()
    yn = input("Are there any other preferences you would like to change? [Y/N]: ")
    valid_choice = False
    while not valid_choice:
        if yn.upper() == "Y":
            valid_choice = True
            update_preferences(user_id, users_df, businesses_df)
        elif yn.upper() == "N":
            valid_choice = True
        else:
            yn = input("INVALID INPUT - Please select Yes [Y] or No [N]: ")