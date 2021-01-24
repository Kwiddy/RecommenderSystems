import datetime
from editReviews import *
from updatePreferences import *
from generateRecommendatations import *


def welcome_page():
    print("|=====================================================|")
    print("|-----------= THE SPORTS BARS RECOMMENDER =-----------|")
    print("|                 ==--- Toronto ---==                 |")
    print("|=====================================================|")
    print()


def select_user(user_df):
    valid_choice = False
    global users_df
    print("[E] - Input an existing user ID")
    print("[S] - Select from pre-chosen user IDs")
    print("[N] - Create new user")
    print("[X] - Exit")
    while not valid_choice:
        input_own_choice = input("Please select from the options above: ")

        if input_own_choice.upper() == "S":
            print()
            valid_choice = True
            print("[A] - fkLVpxbHNmeqgIl7O4GztA (Reviews: 6)")
            print("[B] - deB6EXuanGiN1tkSASuh3A (Reviews: 5)")
            print("[C] - Kj9cFO70zZOQorN0mgeLWA (Reviews: 3)")
            print("[X] - Exit")

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
            return chosen_id

        elif input_own_choice.upper() == "E":
            print()
            valid_input = False
            valid_choice = True
            while not valid_input:
                chosen_id = input("Please enter user ID (or enter [S] to return / [X] to exit): ")
                if chosen_id.upper() == "S":
                    valid_input = True
                    chosen_id = select_user(user_df)
                elif chosen_id.upper() == "X":
                    exit()
                else:
                    user_reviews = user_df[user_df["user_id"] == chosen_id]
                    if len(user_reviews) > 0:
                        valid_input = True
                    else:
                        print("INVALID INPUT - Sorry, it looks like we don't have any users with this ID")
            print()
            return chosen_id

        elif input_own_choice.upper() == "N":
            print()
            valid_choice = True

            # Generate date
            creation_time = str(datetime.datetime.now())[:-7]

            chosen_name = False
            while not chosen_name:
                name = input("Enter first name: ")
                if name.isalpha():
                    chosen_name = True
                else:
                    print("INVALID NAME - Please only include letters in your name")

            user_id = gen_new_user_id(user_df)

            new_user = {"user_id": user_id, "name": name, "review_count": 0, "yelping_since": creation_time,
                        "useful": 0, "funny": 0, "cool": 0, "elite": "", "friends": "None", "fans": 0,
                        "average_stars": 0.0, "compliment_hot": 0, "compliment_more": 0, "compliment_profile": 0,
                        "compliment_cute": 0, "compliment_list": 0, "compliment_note": 0, "compliment_plain": 0,
                        "compliment_cool": 0, "compliment_funny": 0, "compliment_writer": 0, "compliment_photos": 0,
                        "display_num": 12, "blacklist": ""}

            user_df = user_df.append(new_user, ignore_index=True)
            user_df.to_csv("newDFUser.csv", index=0)

            users_df = pd.read_csv("newDFUser.csv")
            # id_search = user_df[user_df["user_id"] == user_id]
            # blacklist = id_search['blacklist'].iloc[0]

            print()
            return user_id

        elif input_own_choice.upper() == "X":
            valid_choice = False
            exit()

        else:
            print("INVALID INPUT")


def gen_new_user_id(users):
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

    return generated_id


def anything_else(user_id):
    print("[M] - Continue")
    print("[L] - Logout and enter another user ID")
    print("[X] - Close the program")
    valid = False
    while not valid:
        choice = input("Please choose one of the options above: ")

        if choice.upper() == "X":
            valid = True
            exit()
        elif choice.upper() == "L":
            valid = True
            print()
            main(True, user_id)
        elif choice.upper() == "M":
            valid = True
            print()
            main(False, user_id)
        elif choice.upper() == "EXIT":
            exit()
        else:
            print("INVALID CHOICE")
    print()


def main(new_user, existing_user):
    global users_df
    users_df = pd.read_csv("newDFUser.csv")

    if new_user:
        i_user_id = select_user(users_df)
    else:
        i_user_id = existing_user

    # Allow user to choose their service
    print("[G] - Generate list of recommendations")
    print("[R] - Add/Amend/View/Delete a Review")
    print("[P] - Update user preferences")
    print("[L] - Logout and enter another User ID")
    print("[X] - Exit")

    valid_choice = False
    while not valid_choice:
        choice = input("Please choose from the services listed above: ")

        if choice.upper() == "G":
            valid_choice = True
            print()
            generate_recommendations(i_user_id, businesses_df, reviews_df, users_df)
        elif choice.upper() == "R":
            valid_choice = True
            print()
            edit_reviews(i_user_id, businesses_df, reviews_df, users_df)
        elif choice.upper() == "P":
            valid_choice = True
            print()
            update_preferences(i_user_id, users_df, businesses_df)
        elif choice.upper() == "L":
            valid_choice= True
            print()
            main(True, i_user_id)
        elif choice.upper() == "X":
            exit()
        else:
            print("INVALID CHOICE - Please select from the list provided")

    anything_else(i_user_id)


businesses_df = pd.read_csv("newDFBusiness.csv")
reviews_df = pd.read_csv("newDFReview.csv")
global users_df

welcome_page()
main(True, "")