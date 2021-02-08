# imports
from editReviews import *
from dataExplanation import *
from updatePreferences import *
from hybridRecommender import *


# Display welcome banner to indicate the startup of the system
def welcome_page():
    print("|=====================================================|")
    print("|-----------= THE SPORTS BARS RECOMMENDER =-----------|")
    print("|                 ==--- Toronto ---==                 |")
    print("|=====================================================|")
    print()


# Allow the user to log in from either: a specific ID, a pre-chosen selection of IDs, or as a new user
def select_user(user_df):
    valid_choice = False
    global users_df

    # Present user login choices
    print("[E] - Input an existing user ID")
    print("[S] - Select from pre-chosen user IDs")
    print("[N] - Create new user")
    print("[X] - Exit")

    # Repeat request for input until a valid input is given
    while not valid_choice:
        input_own_choice = input("Please select from the options above: ")

        # Display a selection of pre-chosen user IDs
        if input_own_choice.upper() == "S":
            print()
            valid_choice = True
            print("[A] - fkLVpxbHNmeqgIl7O4GztA (Reviews: 5)")
            print("[B] - deB6EXuanGiN1tkSASuh3A (Reviews: 4)")
            print("[C] - Kj9cFO70zZOQorN0mgeLWA (Reviews: 1)")
            print("[X] - Exit")

            # Repeat request for input until a valid input is given
            valid = False
            while not valid:
                choice = input("Input the letter corresponding to an ID: ")
                if choice.upper() == "A":
                    chosen_id = "fkLVpxbHNmeqgIl7O4GztA"
                    valid = True
                elif choice.upper() == "B":
                    chosen_id = "deB6EXuanGiN1tkSASuh3A"
                    valid = True
                elif choice.upper() == "C":
                    chosen_id = "Kj9cFO70zZOQorN0mgeLWA"
                    valid = True
                elif choice.upper() == "X":
                    exit()
                else:
                    print("INVALID INPUT")
            print()

            # Return the ID selected from the list
            return chosen_id

        # Allow the user to enter their own user ID
        elif input_own_choice.upper() == "E":
            print()

            # Repeat request for input until input is valid
            valid_input = False
            valid_choice = True
            while not valid_input:
                chosen_id = input("Please enter user ID (or enter [S] to return / [X] to exit): ")

                # Allow the user to return to the main menu and choose a different option
                if chosen_id.upper() == "S":
                    valid_input = True
                    chosen_id = select_user(user_df)

                # Allow user to exit the program
                elif chosen_id.upper() == "X":
                    exit()

                # Check to see if the inputted ID is valid else return an error message
                else:
                    user_reviews = user_df[user_df["user_id"] == chosen_id]
                    if len(user_reviews) > 0:
                        valid_input = True
                    else:
                        print("INVALID INPUT - Sorry, it looks like we don't have any users with this ID")
            print()

            # Return the inputted user ID
            return chosen_id

        # Allow the creation of a new user
        elif input_own_choice.upper() == "N":
            print()
            valid_choice = True

            # Generate date
            creation_time = str(datetime.datetime.now())[:-7]

            # Request the user's name, only accept names with  letters
            chosen_name = False
            while not chosen_name:
                name = input("Enter first name: ")
                if name.isalpha():
                    chosen_name = True
                else:
                    print("INVALID NAME - Please only include letters in your name")

            # Randomly create a new user ID, which is not currently used by another user in the dataset
            user_id = gen_new_user_id(user_df)

            # Create the entry for the new user
            new_user = {"user_id": user_id, "name": name, "review_count": 0, "yelping_since": creation_time,
                        "useful": 0, "funny": 0, "cool": 0, "elite": "", "friends": "None", "fans": 0,
                        "average_stars": 0.0, "compliment_hot": 0, "compliment_more": 0, "compliment_profile": 0,
                        "compliment_cute": 0, "compliment_list": 0, "compliment_note": 0, "compliment_plain": 0,
                        "compliment_cool": 0, "compliment_funny": 0, "compliment_writer": 0, "compliment_photos": 0,
                        "display_num": 12, "blacklist": "", "min_stars": 1, "recommend_seen": "Y"}

            # Append the new user to the users dataset and save
            user_df = user_df.append(new_user, ignore_index=True)
            user_df.to_csv("newDFUser.csv", index=0)

            users_df = pd.read_csv("newDFUser.csv")
            print()

            # Return the new user ID
            return user_id

        # Allow the user to exit the program
        elif input_own_choice.upper() == "X":
            valid_choice = False
            exit()

        # Return an error if no valid option has been chosen
        else:
            print("INVALID INPUT")


# Generate an ID for the new user
def gen_new_user_id(users):
    # Create the alphabet of available characters
    alphabet = list(string.ascii_letters) + ["_", "-"]
    for i in range(0,10):
        alphabet.append(str(i))

    # Generate a random 22 long id which is not already in the users
    valid_selection = False
    while not valid_selection:
        generated_id = ''.join(random.sample(alphabet, 22))
        id_search = users[users["user_id"] == generated_id]

        if len(id_search) == 0:
            valid_selection = True

    # Return the generated ID
    return generated_id


# Ask the user if they require anything else
def anything_else(user_id):
    # Present them with options
    print("[M] - Continue")
    print("[L] - Logout and enter another user ID")
    print("[X] - Close the program")

    # Request an input until a valid input is given
    valid = False
    while not valid:
        choice = input("Please choose one of the options above: ")

        # Allow the user to exit the program
        if choice.upper() == "X":
            valid = True
            exit()

        # Allow the user to logout and for a different user ID to be used
        elif choice.upper() == "L":
            valid = True
            print()
            main(True, user_id)

        # Continue back to the menu to choose another option
        elif choice.upper() == "M":
            valid = True
            print()
            main(False, user_id)

        # Otherwise display error message
        else:
            print("INVALID CHOICE")
    print()


# Main menu where user can choose how to proceed in the system next
def main(new_user, existing_user):
    # read the users dataframe
    global users_df
    users_df = pd.read_csv("newDFUser.csv")

    # Obtain the user ID, requires login if the program has just started
    if new_user:
        i_user_id = select_user(users_df)
    else:
        i_user_id = existing_user

    # Allow user to choose their service
    print("[G] - Generate list of recommendations")
    print("[R] - Add/Amend/View/Delete a Review")
    print("[P] - Update user preferences")
    print("[L] - Logout and enter another User ID")
    print("[H] - How we use your data")
    print("[X] - Exit")

    # Request a valid input until one is given
    valid_choice = False
    while not valid_choice:
        choice = input("Please choose from the services listed above: ")

        # Generate a list of recommendations
        if choice.upper() == "G":
            valid_choice = True
            print()
            generate_recommendations(i_user_id, users_df)

        # Add / Amend / View / Delete a Review
        elif choice.upper() == "R":
            valid_choice = True
            print()
            edit_reviews(i_user_id, businesses_df, reviews_df, users_df)

        # Update user preferences
        elif choice.upper() == "P":
            valid_choice = True
            print()
            update_preferences(i_user_id, users_df, businesses_df)

        # Take user to a page displaying more information about how their data is used
        elif choice.upper() == "H":
            valid_choice = True
            print()
            show_data_explanation()

        # Logout
        elif choice.upper() == "L":
            valid_choice= True
            print()
            main(True, i_user_id)

        # Exit
        elif choice.upper() == "X":
            exit()

        # display error message
        else:
            print("INVALID CHOICE - Please select from the list provided")

    # Ask if the user wishes to do anything else
    anything_else(i_user_id)


# Read dataframes of businesses and reviews and define the global dataframe for users
businesses_df = pd.read_csv("newDFBusiness.csv")
reviews_df = pd.read_csv("newDFReview.csv")
global users_df

# Display the welcome page and begin the program
welcome_page()
main(True, "")