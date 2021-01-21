def edit_reviews(user_id, businesses, reviews, users):
    # Display current reviews
    display_reviews(user_id, reviews)

    # Give the option to Add, Amend, Delete
    print("[N] - Add a new review")
    print("[A] - Amend an existing review")
    print("[D] - Delete an existing review")
    print("[B] - Back")
    print("[X] - Exit")
    valid_choice = False
    while not valid_choice:
        choice = input("Please enter from the selection above: ")

        if choice.upper() == "N":
            valid_choice = True
            add_new_review(user_id)
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "A":
            valid_choice = True
            print("Amend")
            # function to amend existing review
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "D":
            valid_choice = True
            print("delete")
            # function to delete existing review
            anything_else(user_id, businesses, reviews, users)

        elif choice.upper() == "B":
            valid_choice = True
            print()

        elif choice.upper() == "X":
            valid_choice = True
            exit()

        else:
            print("INVALID INPUT")


def add_new_review():
    # Update newDFReview.csv: generate new review id, take user id and business id, take stars, text, and date, add (set other vals to initially zero?)
    # Update newDFBusiness.csv: update review count, do I need to update stars?
    # Update newDFUser.csv: update review count, update average stars,
    # Update newDFCheckin.csv update checkin
    print("HI")


def anything_else(user_id, businesses, reviews, users):
    valid_choice = False
    while not valid_choice:
        yn = input("Continue editing your reviews? [Y/N]: ")
        if yn.upper() == "Y":
            valid_choice = True
            edit_reviews(user_id, businesses, reviews, users)
        elif yn.upper() != "N":
            print("INVALID INPUT")
        else:
            valid_choice = True


def display_reviews(user, reviews):
    user_reviews = reviews[reviews["user_id"] == user]
    print(user_reviews)
    print()