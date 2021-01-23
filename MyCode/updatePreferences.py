
def update_preferences(user_id, users_df):
    print("[N] - Change number of recommendations displayed")
    valid_choice = False
    while not valid_choice:
        selection = input("Please enter one of the options above: ")
        if selection.upper() == "N":
            print()
            valid_choice = True
            update_display_num(user_id, users_df)
        else:
            print("INVALID INPUT")


def update_display_num(user_id, users_df):

    id_search = users_df[users_df["user_id"] == user_id]
    to_display = id_search['display_num'].iloc[0]

    valid_choice = False
    response = input("Please enter the number of recommendations to show (Current: " + str(to_display) + "): ")
    while not valid_choice:
        if response != "":
            try:
                to_display = int(response)
                valid_choice = True
            except ValueError:
                print("INVALID INPUT")
        else:
            valid_choice = True

    users_df.loc[users_df["user_id"] == user_id, "display_num"] = to_display
    print("Preferred number of recommendations changed to: ", to_display)
    anything_else(user_id, users_df)
    users_df.to_csv("newDFUser.csv", index=0)


def anything_else(user_id, users_df):
    print()
    yn = input("Are there any other preferences you would like to change? [Y/N]: ")
    valid_choice = False
    while not valid_choice:
        if yn.upper() == "Y":
            valid_choice = True
            update_preferences(user_id, users_df)
        elif yn.upper() == "N":
            valid_choice = True
        else:
            yn = input("INVALID INPUT - Please select Yes [Y] or No [N]: ")