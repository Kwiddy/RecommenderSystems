from editReviews import *
from generateRecommendatations import *


def select_user(user_df):
    valid_choice = False
    while not valid_choice:
        input_own_choice = input("Please enter [N] for inputting a chosen user id, or [S] to select from pre-chosen IDs: ")

        if input_own_choice.upper() == "S":
            valid_choice = True
            print("[A] 2U2tqOCphgOQ-NX8b3P6nw")
            print("[B] UHkDeBOmSKQCBIi9t8YzJw")
            print("[C] deB6EXuanGiN1tkSASuh3A")
            print("[X] - Exit")

            valid = False
            while not valid:
                choice = input("Input the letter corresponding to an ID: ")
                if choice.upper() == "A":
                    chosen_id = "2U2tqOCphgOQ-NX8b3P6nw"
                    valid = True
                elif choice.upper() == "B":
                    chosen_id = "UHkDeBOmSKQCBIi9t8YzJw"
                    valid = True
                elif choice.upper() == "C":
                    chosen_id = "deB6EXuanGiN1tkSASuh3A"
                    valid = True
                elif choice.upper() == "X":
                    exit()
                else:
                    print("INVALID INPUT")
            print()
            return chosen_id

        elif input_own_choice.upper() == "N":
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
        else:
            print("INVALID INPUT")


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
    if new_user:
        i_user_id = select_user(users_df)
    else:
        i_user_id = existing_user

    # Allow user to choose their service
    print("[G] - Generate list of recommendations")
    print("[R] - Add/Amend/Delete a Review")
    print("[P] - Update user preferences")
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
        elif choice.upper() == "X":
            exit()
        else:
            print("INVALID CHOICE - Please select from the list provided")

    anything_else(i_user_id)


businesses_df = pd.read_csv("newDFBusiness.csv")
reviews_df = pd.read_csv("newDFReview.csv")
users_df = pd.read_csv("newDFUser.csv")

main(True, "")